from django.views import View
from django.shortcuts import render, redirect
from apps.modular_engine.services.module_service import ModuleService
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from apps.core.utils import has_role

@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class ModuleListView(View):
    def get(self, request):
        if not has_role(request.user, ['Manager']):
            raise PermissionDenied

        modules = ModuleService.list_modules()
        return render(request, 'modular_engine/module_list.html', {'modules': modules})


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class InstallModuleView(View):
    def post(self, request, module_id):
        if not has_role(request.user, ['Manager']):
            raise PermissionDenied

        ModuleService.install_module(module_id)
        return redirect('module_list')


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class UninstallModuleView(View):
    def post(self, request, module_id):
        if not has_role(request.user, ['Manager']):
            raise PermissionDenied

        ModuleService.uninstall_module(module_id)
        return redirect('module_list')


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class UpgradeModuleView(View):
    def post(self, request, module_id):
        if not has_role(request.user, ['Manager']):
            raise PermissionDenied

        ModuleService.upgrade_module(module_id, request)

        return redirect('module_list')
