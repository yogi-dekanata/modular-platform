from django.test import TestCase, override_settings
from unittest.mock import patch, MagicMock
import subprocess

from apps.modular_engine.services.module_migration_service import ModuleMigrationService


@override_settings(BASE_DIR="/fake/path")
class TestModuleMigrationService(TestCase):
    @patch("subprocess.run")
    def test_safe_makemigrations_success(self, mock_run):
        mock_run.return_value.returncode = 0
        result = ModuleMigrationService.safe_makemigrations('product_management')
        self.assertTrue(result)

    @patch("subprocess.run")
    def test_safe_makemigrations_failure_due_to_non_nullable_field(self, mock_run):
        mock_run.return_value.returncode = 1
        mock_run.return_value.stdout = "It is impossible to add a non-nullable field"
        mock_run.return_value.stderr = ""

        with self.assertRaises(Exception) as context:
            ModuleMigrationService.safe_makemigrations('product_management')
        self.assertIn("Cannot upgrade", str(context.exception))

    @patch("subprocess.run")
    @patch("os.path.isdir", return_value=True)
    def test_migrate_module_success(self, mock_isdir, mock_run):
        mock_run.return_value.returncode = 0
        try:
            ModuleMigrationService.migrate_module('product_management')
        except Exception:
            self.fail("migrate_module() raised Exception unexpectedly!")

    @patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "cmd"))
    @patch("os.path.isdir", return_value=True)
    def test_migrate_module_failure(self, mock_isdir, mock_run):
        with self.assertRaises(Exception) as context:
            ModuleMigrationService.migrate_module('product_management')
        self.assertIn("Migration failed", str(context.exception))

    def test_fake_unmigrate(self):
        # Should simply not raise error
        ModuleMigrationService.fake_unmigrate('product_management')
