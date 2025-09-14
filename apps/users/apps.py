"""ZZZ"""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    """ZZZ"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'
    app_label = 'users'
    verbose_name = _('Users Management')
