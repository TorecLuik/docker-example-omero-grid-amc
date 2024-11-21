from django.urls import path
from . import views

urlpatterns = [
    # Import page URLs
    path('server_side_browser/', views.server_side_browser_page, name='server_side_browser_page'),
    path('api/list_dir/', views.list_directory, name='list_directory'),
    path('api/file_info/', views.file_info, name='file_info'),
    path('api/import_selected/', views.import_selected, name='import_selected'),
    
    # Database page URLs
    path('imports/', views.imports_database_page, name='imports_database_page'),
    path('workflows/', views.workflows_database_page, name='workflows_database_page'),
    
    # Script menu URLs
    path('script_menu/', views.script_menu_page, name='script_menu_page'),
    path('api/list_scripts/', views.list_scripts, name='list_scripts'),
    path('api/run_script/', views.run_script, name='run_script'),
]