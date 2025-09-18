"""Custom User Model"""
from django.contrib.auth.models import AbstractUser, Group
from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """Custom User Model"""

    # Override username to set default
    username = models.CharField(max_length=150, unique=True, default='defaultuser')

    # Use email as additional field
    email = models.EmailField(_("email address"), unique=True)

    ROLE_CHOICES = [
        ('cliente', 'Cliente'),
        ('trabajador', 'Trabajador'),
        ('admin', 'Administrador'),
        ('superadmin', 'Superadministrador')
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='cliente')

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = CustomUserManager()

    class Meta:
        """Meta class for CustomUser model"""
        db_table = 'custom_user'
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        """String representation of the user"""
        return self.email

    def get_absolute_url(self):
        """Get absolute URL for the user detail view"""
        return reverse("CustomUser_detail", kwargs={"pk": self.pk})


class GroupProxy(Group):
    """Proxy model for Django's Group model."""
    class Meta:
        """Meta class for GroupProxy model."""
        proxy = True
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")
