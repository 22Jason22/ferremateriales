
"""
Custom management command to clean the project.
"""
import os
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.utils.translation import gettext_lazy as _

# pylint: disable=no-member


class Command(BaseCommand):
    """
    Cleans the project, deletes the database, and runs migrations.
    """
    help = _('Cleans the project, deletes the database, and runs migrations.')

    def handle(self, *args, **options):
        base_dir = settings.BASE_DIR
        self.stdout.write(self.style.SUCCESS(_('Starting project cleanup...')))

        # Find and delete temporary files and directories
        for root, dirs, files in os.walk(base_dir):
            for name in files:
                if name.endswith('.pyc'):
                    os.remove(os.path.join(root, name))
                    self.stdout.write(_(f'Removed {os.path.join(root, name)}'))
            for name in dirs:
                if name == '__pycache__':
                    shutil.rmtree(os.path.join(root, name))
                    self.stdout.write(_(f'Removed {os.path.join(root, name)}'))

        self.stdout.write(self.style.SUCCESS(
            _('Temporary files and directories removed.')))

        # Delete the SQLite database file
        db_path = settings.DATABASES['default']['NAME']
        if os.path.exists(db_path):
            os.remove(db_path)
            self.stdout.write(self.style.SUCCESS(
                _(f'Database file {db_path} removed.')))

        # Create and run migrations
        self.stdout.write(self.style.SUCCESS(_('Creating migrations...')))
        call_command('makemigrations')
        self.stdout.write(self.style.SUCCESS(_('Running migrations...')))
        call_command('migrate')

        self.stdout.write(self.style.SUCCESS(
            _('Project cleanup, database reset, and migrations complete.')))
