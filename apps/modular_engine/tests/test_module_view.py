from unittest import TestCase
from unittest.mock import patch, MagicMock
from django.test import RequestFactory
from django.contrib.auth.models import User
from apps.modular_engine.views.module_view import (
    ModuleListView, InstallModuleView, UninstallModuleView, UpgradeModuleView
)

class TestModuleListView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='manager1', password='password')

    @patch('apps.modular_engine.views.module_view.has_role')
    @patch('apps.modular_engine.views.module_view.ModuleService.list_modules')
    def test_get(self, mock_list_modules, mock_has_role):
        mock_has_role.return_value = True

        class DummyModule:
            id = 1

        mock_list_modules.return_value = [DummyModule()]

        request = self.factory.get('/modules/')
        request.user = self.user

        response = ModuleListView.as_view()(request)

        self.assertEqual(response.status_code, 200)


class TestInstallModuleView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='manager2', password='password')

    @patch('apps.modular_engine.views.module_view.has_role')
    @patch('apps.modular_engine.views.module_view.ModuleService.install_module')
    def test_post(self, mock_install_module, mock_has_role):
        mock_has_role.return_value = True

        request = self.factory.post('/modules/install/1/')
        request.user = self.user

        response = InstallModuleView.as_view()(request, module_id=1)

        self.assertEqual(response.status_code, 302)

class TestUninstallModuleView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='manager3', password='password')

    @patch('apps.modular_engine.views.module_view.has_role')
    @patch('apps.modular_engine.views.module_view.ModuleService.uninstall_module')
    def test_post(self, mock_uninstall_module, mock_has_role):
        mock_has_role.return_value = True

        request = self.factory.post('/modules/uninstall/1/')
        request.user = self.user

        response = UninstallModuleView.as_view()(request, module_id=1)

        self.assertEqual(response.status_code, 302)

class TestUpgradeModuleView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='manager4', password='password')

    @patch('apps.modular_engine.views.module_view.has_role')
    @patch('apps.modular_engine.views.module_view.ModuleService.upgrade_module')
    def test_post(self, mock_upgrade_module, mock_has_role):
        mock_has_role.return_value = True

        request = self.factory.post('/modules/upgrade/1/')
        request.user = self.user

        response = UpgradeModuleView.as_view()(request, module_id=1)

        self.assertEqual(response.status_code, 302)
