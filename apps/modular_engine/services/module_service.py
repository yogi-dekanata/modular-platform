import subprocess
from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
from packaging import version

from apps.modular_engine.models.module import Module
from apps.modular_engine.repositories.module_repository import ModuleRepository
from apps.modular_engine.services.module_migration_service import ModuleMigrationService


class ModuleService:

    @staticmethod
    def list_modules():
        return ModuleRepository.get_all_modules()

    @staticmethod
    def install_module(module_id):
        try:
            with transaction.atomic():
                module = ModuleRepository.install_module(module_id)

                app_label = f"{module.slug}"

                subprocess.run(['python', 'manage.py', 'makemigrations', app_label], check=True)
                subprocess.run(['python', 'manage.py', 'migrate', app_label, '--noinput'], check=True)

                module.status = 'installed'
                module.save(update_fields=["status"])

                return module

        except subprocess.CalledProcessError as exc:
            raise Exception(f"❌ Failed to install module: {exc}")

        except Exception as exc:
            raise Exception(f"❌ General install module error: {exc}")

    @staticmethod
    def uninstall_module(module_id):
        try:
            with transaction.atomic():
                module = Module.objects.select_for_update().get(id=module_id)

                if module.status != 'installed':
                    raise Exception(f"Module {module.name} is not installed.")

                module.status = 'uninstalled'
                module.save(update_fields=["status"])

                if module.slug == 'product_management':
                    ModuleMigrationService.fake_unmigrate('apps.product_management')

                return module

        except Module.DoesNotExist:
            raise Exception(f"Module with ID {module_id} not found.")

        except Exception as exc:
            raise Exception(f"Failed to uninstall module: {exc}")

    @staticmethod
    def upgrade_module(module_id: int, request):
        module = Module.objects.get(id=module_id)

        try:
            with transaction.atomic():
                ModuleMigrationService.safe_makemigrations(module.slug)
                ModuleMigrationService.migrate_module(module.slug)

                # Auto upgrade version
                current_version = version.parse(module.version)
                new_version = f"{current_version.major}.{current_version.minor + 1}"
                module.version = new_version
                module.status = 'installed'
                module.save(update_fields=["version", "status"])

                messages.success(request, f"✅ {module.name} upgraded successfully to version {new_version}")

        except Exception as exc:
            print(exc)
            messages.error(request, f"❌ Failed to upgrade {module.name}. Please check your fields or contact admin.")
            return redirect('module_list')
