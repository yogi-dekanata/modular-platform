from unittest import TestCase
from unittest.mock import patch, MagicMock
from apps.modular_engine.services.module_service import ModuleService


class TestModuleService(TestCase):
    @patch('apps.modular_engine.repositories.module_repository.ModuleRepository.get_all_modules')
    def test_list_modules(self, mock_get_all_modules):
        mock_get_all_modules.return_value = ['dummy_module']
        result = ModuleService.list_modules()
        self.assertEqual(result, ['dummy_module'])

    @patch('apps.modular_engine.services.module_service.subprocess.run')
    @patch('apps.modular_engine.repositories.module_repository.ModuleRepository.install_module')
    def test_install_module(self, mock_install_module, mock_subprocess_run):
        dummy_module = MagicMock(slug='dummy')
        mock_install_module.return_value = dummy_module
        mock_subprocess_run.return_value.returncode = 0

        result = ModuleService.install_module(1)
        self.assertEqual(result.status, 'installed')

    @patch('apps.modular_engine.services.module_service.Module.objects.select_for_update')
    @patch('apps.modular_engine.services.module_service.ModuleMigrationService.fake_unmigrate')
    def test_uninstall_module(self, mock_fake_unmigrate, mock_select_for_update):
        dummy_module = MagicMock()
        dummy_module.status = 'installed'
        mock_select_for_update.return_value.get.return_value = dummy_module

        result = ModuleService.uninstall_module(1)
        self.assertEqual(result.status, 'uninstalled')

    @patch('apps.modular_engine.services.module_service.messages')
    @patch('apps.modular_engine.services.module_service.transaction.atomic')
    @patch('apps.modular_engine.services.module_service.ModuleMigrationService.migrate_module')
    @patch('apps.modular_engine.services.module_service.ModuleMigrationService.safe_makemigrations')
    @patch('apps.modular_engine.services.module_service.Module.objects.get')
    def test_upgrade_module(self, mock_get_module, mock_safe_makemigrations, mock_migrate_module, mock_atomic, mock_messages):
        dummy_module = MagicMock()
        dummy_module.version = '1.0'
        dummy_module.name = 'Dummy Module'
        dummy_module.status = 'installed'
        mock_get_module.return_value = dummy_module

        request = MagicMock()

        ModuleService.upgrade_module(1, request)

        self.assertEqual(dummy_module.version, '1.1')
