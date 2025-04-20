from django.urls import path
from apps.modular_engine.views.module_view import ModuleListView, InstallModuleView, UninstallModuleView, UpgradeModuleView

urlpatterns = [
    path('', ModuleListView.as_view(), name='module_list'),
    path('install/<int:module_id>/', InstallModuleView.as_view(), name='install_module'),
    path('uninstall/<int:module_id>/', UninstallModuleView.as_view(), name='uninstall_module'),
    path('upgrade/<int:module_id>/', UpgradeModuleView.as_view(), name='upgrade_module'),
]
