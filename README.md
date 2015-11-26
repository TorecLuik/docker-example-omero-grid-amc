OMERO.grid Docker
=================

This is an example of using OMERO on multiple nodes (such as running the Processor service on a separate node from the main OMERO.server), based on
http://www.openmicroscopy.org/site/support/omero5/sysadmins/grid.html#nodes-on-multiple-hosts


Building the images
-------------------

    ./build.py omero-grid
    ./build.py omero-grid-web

This will automatically build and tag the images as `openmicroscopy/omero-grid:latest` and `openmicroscopy/omero-grid-web:latest`.


Running the images
------------------

To run the Docker images start a postgres DB:

    docker run -d --name postgres -e POSTGRES_PASSWORD=postgres postgres

Then either run a single all-in-one master:

    docker run -it --rm --link postgres:db -e DBUSER=postgres -e DBPASS=postgres \
        -e DBNAME=postgres --name omero-master openmicroscopy/omero-grid master

Or run a master and one or more slaves, the configuration must be provided to the master node.
For example, to run two Processors on separate slaves and all other servers on master:

    docker run -it --rm --link postgres:db \
        -e DBUSER=postgres -e DBPASS=postgres -e DBNAME=postgres \
        --name omero-master openmicroscopy/omero-grid master \
        master:Blitz-0,Indexer-0,DropBox,MonitorServer,FileServer,Storm,PixelData-0,Tables-0,TestDropBox \
        slave-1:Processor-0 slave-2:Processor-1
    docker run -it --rm --link omero-master:master omero-grid slave-1
    docker run -it --rm --link omero-master:master omero-grid slave-2

Finally run the web client:

    docker run -it --rm --link omero-master:master openmicroscopy/omero-grid-web


Configuration files
-------------------

Additional configuration files for OMERO can be provided by mounting a directory `/config` inside any of the containers.
Files will be loaded with `omero load`.
For example:

    docker run -it --rm --link omero-master:master \
        -v /config/master:/config:ro openmicroscopy/omero-grid master

The OMERO.web nginx config file will be autogenerated at runtime if `/etc/nginx/conf.d/omero-web.conf` does not exist, so for example you can set a custom prefix in a file under `/config` and the template will be generated correctly.

If you want to manage the full nginx configuration outside Docker than mount `/etc/nginx`.


Custom OMERO builds
-------------------

These images default to using the latest release build of OMERO.
You can override the version/branch, and/or the continuous integration server, see `./build.py --help` for details.

The images will be tagged (`<user>/<image>:<tag>`) with a different user (based on the CI server if not the default) and tag (the release version or branch name) to indicate they are using a non-standard version of OMERO.

In addition `omego` args can also be passed, if this is done the image name will be prefixed with `x-`.
