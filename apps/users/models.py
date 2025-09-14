"""Custom User Model"""
from django.contrib.auth.models import AbstractUser, Group
from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """Custom User Model that uses email as the username field"""

    # Remove default first_name, and last_name fields
    first_name = None
    last_name = None

    # Use email as the unique identifier
    email = models.EmailField(_("email address"), unique=True)

    username = None # Remove username field as email is used for authentication
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

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
