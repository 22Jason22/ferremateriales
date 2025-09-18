"""zzz"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class Customer(models.Model):
    """
    Model that represents a customer.
    """
    class ClientType(models.TextChoices):
        CONSTRUCTORA = 'construction_company', _('Construction Company')
        FERRETERIA = 'hardware_store', _('Hardware Store')
        PUBLICO_GENERAL = 'general_public', _('General Public')
        OTROS = 'other', _('Other')

    class Status(models.TextChoices):
        ACTIVO = 'active', _('Active')
        INACTIVO = 'inactive', _('Inactive')
        MOROSO = 'delinquent', _('Delinquent')
        NUEVO = 'new', _('New')

    name = models.CharField(
        _("Name"),
        max_length=255,
        help_text=_("The full name or business name of the customer."),
    )
    tax_id = models.CharField(
        _("Tax ID"),
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        help_text=_("The tax identification number (e.g., RUC) of the customer."),
    )
    contact_name = models.CharField(
        _("Contact Name"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The name of the main contact person for the customer."),
    )
    email = models.EmailField(
        _("Email"),
        unique=True,
        blank=True,
        null=True,
        help_text=_("The main email address of the customer."),
    )
    phone = models.CharField(
        _("Phone"),
        max_length=20,
        blank=True,
        null=True,
        help_text=_("The primary phone number of the customer."),
    )
    address = models.TextField(
        _("Address"),
        blank=True,
        null=True,
        help_text=_("The physical address of the customer."),
    )
    client_type = models.CharField(
        _("Client Type"),
        max_length=50,
        choices=ClientType.choices,
        default=ClientType.CONSTRUCTORA,
        help_text=_("The type of client, e.g., 'Construction Company'."),
    )
    status = models.CharField(
        _("Status"),
        max_length=50,
        choices=Status.choices,
        default=Status.ACTIVO,
        help_text=_("The current status of the customer."),
    )
    last_purchase = models.DateTimeField(
        _("Last Purchase"),
        blank=True,
        null=True,
        help_text=_("The date and time of the customer's last purchase."),
    )
    created_at = models.DateTimeField(
        _("Created At"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _("Updated At"),
        auto_now=True,
    )

    class Meta:
        """
        Meta configuration for the Customer model.
        """
        db_table = "customers"
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")

    def __str__(self):
        return self.name


class Supplier(models.Model):
    """
    Model that represents a supplier.
    """
    class Rubro(models.TextChoices):
        CONSTRUCCION = 'construccion', _('Construcción')
        FERRETERIA = 'ferreteria', _('Ferretería')
        MATERIALES = 'materiales', _('Materiales')
        OTROS = 'otros', _('Otros')

    class PlazoPago(models.TextChoices):
        CONTADO = 'contado', _('Contado')
        DIAS_15 = '15_dias', _('15 días')
        DIAS_30 = '30_dias', _('30 días')
        DIAS_60 = '60_dias', _('60 días')
        DIAS_90 = '90_dias', _('90 días')

    class Estado(models.TextChoices):
        ACTIVO = 'activo', _('Activo')
        SUSPENDIDO = 'suspendido', _('Suspendido')
        INACTIVO = 'inactivo', _('Inactivo')

    razon_social = models.CharField(
        _("Razón Social"),
        max_length=255,
        default='',
    )
    ruc = models.CharField(
        _("RUC"),
        max_length=50,
        unique=True,
        blank=True,
        null=True,
    )
    rubro = models.CharField(
        _("Rubro"),
        max_length=50,
        choices=Rubro.choices,
        default=Rubro.CONSTRUCCION,
    )
    telefono = models.CharField(
        _("Teléfono"),
        max_length=20,
        blank=True,
        null=True,
    )
    contacto_nombre = models.CharField(
        _("Nombre de Contacto"),
        max_length=255,
        blank=True,
        null=True,
    )
    contacto_email = models.EmailField(
        _("Email de Contacto"),
        blank=True,
        null=True,
    )
    contacto_telefono = models.CharField(
        _("Teléfono de Contacto"),
        max_length=20,
        blank=True,
        null=True,
    )
    direccion = models.TextField(
        _("Dirección"),
        blank=True,
        null=True,
    )
    plazo_pago = models.CharField(
        _("Plazo de Pago"),
        max_length=50,
        choices=PlazoPago.choices,
        default=PlazoPago.DIAS_30,
    )
    estado = models.CharField(
        _("Estado"),
        max_length=50,
        choices=Estado.choices,
        default=Estado.ACTIVO,
    )
    certificado = models.BooleanField(
        _("Certificado"),
        default=False,
        help_text=_("Proveedor certificado"),
    )
    created_at = models.DateTimeField(
        _("Created At"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _("Updated At"),
        auto_now=True,
    )

    class Meta:
        """
        Meta configuration for the Supplier model.
        """
        db_table = "suppliers"
        verbose_name = _("Supplier")
        verbose_name_plural = _("Suppliers")

    def __str__(self):
        return self.razon_social or "Sin nombre"


class Lead(models.Model):
    """
    Model that represents a lead.
    """
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="leads"
    )
    source = models.CharField(
        _("Source"),
        max_length=255,
        blank=True,
        null=True,
    )
    status = models.CharField(
        _("Status"),
        max_length=100,
        blank=True,
        null=True,
    )
    status = models.CharField(
        _("Status"),
        max_length=100,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        _("Created At"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _("Updated At"),
        auto_now=True,
    )

    class Meta:
        """
        Meta configuration for the Lead model."""
        db_table = "leads"
        verbose_name = _("Lead")
        verbose_name_plural = _("Leads")

    def __str__(self):
        return f"{self.customer.name} - {self.status or 'No status'}"