from unittest import TestCase
from unittest.mock import patch, MagicMock
from apps.modular_engine.repositories.module_repository import ModuleRepository

class ModuleRepositoryTest(TestCase):
    @patch('apps.modular_engine.repositories.module_repository.Module')
    def test_install_module(self, mock_module):
        mock_instance = MagicMock()
        mock_module.objects.get.return_value = mock_instance

        result = ModuleRepository.install_module(1)

        mock_module.objects.get.assert_called_once_with(id=1)
        self.assertEqual(result, mock_instance)
        self.assertEqual(mock_instance.status, 'installed')
        self.assertIsNotNone(mock_instance.installed_date)
        mock_instance.save.assert_called_once()

    @patch('apps.modular_engine.repositories.module_repository.Module')
    def test_uninstall_module(self, mock_module):
        mock_instance = MagicMock()
        mock_module.objects.get.return_value = mock_instance

        result = ModuleRepository.uninstall_module(1)

        mock_module.objects.get.assert_called_once_with(id=1)
        self.assertEqual(result, mock_instance)
        self.assertEqual(mock_instance.status, 'uninstalled')
        mock_instance.save.assert_called_once()

    @patch('apps.modular_engine.repositories.module_repository.Module')
    def test_upgrade_module(self, mock_module):
        mock_instance = MagicMock()
        mock_instance.version = '1.0'
        mock_module.objects.get.return_value = mock_instance

        result = ModuleRepository.upgrade_module(1)

        mock_module.objects.get.assert_called_once_with(id=1)
        self.assertEqual(result, mock_instance)
        self.assertEqual(mock_instance.version, '1.1')
        mock_instance.save.assert_called_once()
