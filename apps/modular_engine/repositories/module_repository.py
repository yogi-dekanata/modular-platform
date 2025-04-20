from apps.modular_engine.models.module import Module
from django.utils import timezone

class ModuleRepository:

    @staticmethod
    def get_all_modules():
        return Module.objects.all()

    @staticmethod
    def install_module(module_id):
        module = Module.objects.get(id=module_id)
        module.status = 'installed'
        module.installed_date = timezone.now()
        module.save()
        return module

    @staticmethod
    def uninstall_module(module_id):
        module = Module.objects.get(id=module_id)
        module.status = 'uninstalled'
        module.save()
        return module

    @staticmethod
    def upgrade_module(module_id):
        module = Module.objects.get(id=module_id)
        # Simulasikan upgrade version simple
        current_version = float(module.version)
        module.version = str(round(current_version + 0.1, 1))
        module.save()
        return module
