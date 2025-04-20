import subprocess
import os
import shutil
from django.conf import settings

class ModuleMigrationService:

    @staticmethod
    def safe_makemigrations(app_slug):
        """
        Cek apakah ada perubahan model yang butuh makemigrations.
        Kalau ada perubahan, itu valid.
        """
        try:
            result = subprocess.run(
                ["python", "manage.py", "makemigrations", app_slug, "--check", "--dry-run"],
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                return True
            else:
                stdout = (result.stdout or '').strip()
                stderr = (result.stderr or '').strip()

                if "It is impossible to add a non-nullable field" in stdout or "It is impossible to add a non-nullable field" in stderr:
                    raise Exception("Cannot upgrade: You must set a default value or allow null on new fields.")

                return True

        except subprocess.CalledProcessError as e:
            raise Exception(f"Cannot validate makemigrations. [Internal error: {e.stderr or e.stdout}]")

    @staticmethod
    def fake_unmigrate(app_slug):
        """Placeholder fake unmigrate."""
        pass

    @staticmethod
    def migrate_module(app_slug: str):
        """
        Backup migrations → run makemigrations & migrate → rollback kalau error.
        """

        app_path = os.path.join(settings.BASE_DIR, 'apps', app_slug)
        if not os.path.isdir(app_path):
            app_path = os.path.join(settings.BASE_DIR.parent, 'apps', app_slug)

        if not os.path.isdir(app_path):
            raise Exception(f"App folder 'apps/{app_slug}' does not exist.")


        migrations_dir = os.path.join(app_path, 'migrations')

        try:
            if os.path.exists(migrations_dir):
                backup_dir = migrations_dir + "_backup"
                if os.path.exists(backup_dir):
                    shutil.rmtree(backup_dir)
                shutil.copytree(migrations_dir, backup_dir)

            subprocess.run(["python", "manage.py", "makemigrations", f"{app_slug}"], check=True)
            subprocess.run(["python", "manage.py", "migrate", f"{app_slug}", "--noinput"], check=True)

        except subprocess.CalledProcessError as e:
            if os.path.exists(migrations_dir + "_backup"):
                if os.path.exists(migrations_dir):
                    shutil.rmtree(migrations_dir)
                shutil.move(migrations_dir + "_backup", migrations_dir)

            raise Exception(f"Migration failed: {e}")

        finally:
            if os.path.exists(migrations_dir + "_backup"):
                shutil.rmtree(migrations_dir + "_backup")
