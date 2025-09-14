"""Core models for the Nexus project."""
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


class BaseModel(models.Model):
    """Base model with common fields."""
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        """Meta class for the base model."""
        abstract = True


class ChangeLog(models.Model):
    """Model to track changes."""
    changed_by = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True, blank=True)
    change_date = models.DateTimeField(default=timezone.now)
    change_description = models.TextField(blank=True)

    class Meta:
        """Meta class for the change log model."""
        verbose_name = _("Change Log")
        verbose_name_plural = _("Change Logs")


class User(AbstractUser, BaseModel):
    """User model extending AbstractUser."""
    # GuardianUserMixin removed due to import issues

    def __str__(self):
        return str(self.username)


class Person(BaseModel):
    """Person model."""
    first_name = models.CharField(_("First Name"), max_length=150)
    last_name = models.CharField(_("Last Name"), max_length=150)
    birth_date = models.DateField(_("Birth Date"), null=True, blank=True)

    def __str__(self):
        return str(f"{self.first_name} {self.last_name}")


class ContactInfo(BaseModel):
    """Contact information for a person."""
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="contact_infos")
    email = models.EmailField(_("Email"), blank=True)
    phone = models.CharField(_("Phone"), max_length=20, blank=True)

    def __str__(self):
        return str(self.email or self.phone or "Contact Info")


class EmergencyContactInfo(BaseModel):
    """Emergency contact information for a person."""
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="emergency_contacts")
    name = models.CharField(_("Name"), max_length=150)
    phone = models.CharField(_("Phone"), max_length=20)

    def __str__(self):
        return str(f"{self.name} ({self.phone})")
