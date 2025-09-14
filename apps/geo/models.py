"""Models for geographical entities."""
from django.db import models
from django.utils.translation import gettext_lazy as _


class Country(models.Model):
    """
    Modelo que representa un país.
    """
    name = models.CharField(
        _("Country"),
        max_length=255,
    )

    class Meta:
        """
        Meta configuration for the Country model.
        """
        db_table = "countries"
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")

    def __str__(self):
        return str(self.name)


class Federalstate(models.Model):
    """
    Modelo que representa un estado federativo.
    """
    name = models.CharField(
        _("Federalstate"),
        max_length=255,
    )

    class Meta:
        """
        Meta configuration for the Federalstate model.
        """
        db_table = "federalstates"
        verbose_name = _("Federalstate")
        verbose_name_plural = _("Federalstates")

    def __str__(self):
        return str(self.name)


class Municipality(models.Model):
    """
    Modelo que representa una municipalidad.
    """
    name = models.CharField(
        _("Municipality"),
        max_length=255,
    )

    class Meta:
        """
        Meta configuration for the Municipality model.
        """""
        db_table = "municipalities"
        verbose_name = _("Municipality")
        verbose_name_plural = _("Municipalities")

    def __str__(self):
        return str(self.name)


class Parish(models.Model):
    """
    Modelo que representa una parroquia.
    """
    name = models.CharField(
        _("Parish"),
        max_length=255,
    )

    class Meta:
        """
        Meta configuration for the Parish model."""
        db_table = "parishes"
        verbose_name = _("Parish")
        verbose_name_plural = _("Parishes")

    def __str__(self):
        return str(self.name)


class PostalCode(models.Model):
    """Modelo que representa un código postal."""
    code = models.CharField(_("Postal Code"), max_length=20)

    class Meta:
        """Meta configuration for the PostalCode model."""
        db_table = "postal_codes"
        verbose_name = _("Postal Code")
        verbose_name_plural = _("Postal Codes")

    def __str__(self):
        return str(self.code)


class LandlinePrefix(models.Model):
    """Modelo que representa un prefijo de teléfono fijo."""
    prefix = models.CharField(
        _("Landline Prefix"),
        max_length=10,
    )

    class Meta:
        """Meta configuration for the LandlinePrefix model."""
        db_table = "landline_prefixes"
        verbose_name = _("Landline Prefix")
        verbose_name_plural = _("Landline Prefixes")

    def __str__(self):
        return str(self.prefix)
