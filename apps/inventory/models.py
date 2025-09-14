"""
Inventory models.
"""
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.conf import settings # Needed for AUTH_USER_MODEL
from PIL import Image


class Category(models.Model):
    """
    Model representing a product category.
    """
    CATEGORY_CHOICES = [
        ('Pisos', 'pisos'),
        ('Cocinas', 'cocinas'),
        ('Construcción', 'construcción'),
        ('Maderas y Puertas', 'maderas y puertas'),
        ('Limpieza', 'limpieza'),
        ('Ferretería y Cerrajería', 'ferretería y cerrajería'),
        ('Electrodomésticos', 'electrodomésticos'),
        ('Exteriores', 'exteriores'),
        ('Muebles y Organización', 'muebles y organización'),
        ('Pinturas', 'pinturas'),
        ('Baños', 'baños'),
        ('Plomería', 'plomería'),
        ('Seguridad', 'seguridad'),
        ('Lámparas', 'lámparas'),
        ('Herramientas', 'herramientas'),
        ('Electricidad', 'electricidad'),
        ('Decoración', 'decoración'),
        ('Automotriz', 'automotriz'),
    ]

    name = models.CharField(
        _("Name"),
        max_length=100,
        unique=True,
        choices=CATEGORY_CHOICES
    )

    class Meta:
        """
        Meta configuration for the Category model.
        """
        app_label = "inventory"
        db_table = "categories"
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    """
    Model representing a product.
    """
    name = models.CharField(
        _("Name"),
        max_length=100,
        unique=True
    )
    unit = models.CharField(
        _("Unit"),
        max_length=50
    )
    category = models.ForeignKey(
        'Category',
        verbose_name=_("Category"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    price = models.DecimalField(
        _("Price"),
        max_digits=10,
        decimal_places=2,
        default=0.00
    )
    discount_percent = models.PositiveIntegerField(
        _("Discount Percent"),
        default=0,
        help_text=_("Discount percentage for the product")
    )
    is_new = models.BooleanField(
        _("Is New"),
        default=False,
        help_text=_("Designates whether the product is new")
    )
    current_stock = models.DecimalField(
        _("Current Stock"),
        max_digits=10,
        decimal_places=2
    )
    description = models.TextField(
        _("Description"),
        blank=True,
        help_text=_("Detailed description of the product")
    )
    image = models.ImageField(
        _("Product Image"),
        upload_to='product_images/',
        null=True,
        blank=True
    )

    class Meta:
        """
        Meta configuration for the Product model.
        """
        app_label = "inventory"
        db_table = "products"
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        """
        Return the URL to access a detail record for this product.
        """
        return reverse("product_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 300 or img.width > 400:
                # Resize to fit within 400x300, maintaining aspect ratio
                img.thumbnail((400, 300))
                img.save(self.image.path)


class StockMovement(models.Model):
    """
    Model representing a stock movement.
    """
    STOCK_MOVEMENT_TYPE_CHOICES = [
        (True, _("In")),
        (False, _("Out")),
    ]

    REASON_CHOICES = [
        ('purchase', _('Purchase')),
        ('sale', _('Sale')),
        ('adjustment', _('Adjustment')),
        ('return', _('Return')),
        ('damage', _('Damage')),
    ]

    stock_movement_type = models.BooleanField(
        _("Stock Movement Type"),
        choices=STOCK_MOVEMENT_TYPE_CHOICES,
        default=True
    )
    product = models.ForeignKey(
        Product,
        verbose_name=_("Product"),
        on_delete=models.CASCADE
    )
    quantity = models.DecimalField(
        _("Quantity"),
        max_digits=10,
        decimal_places=2
    )
    date = models.DateField(
        _("Date"),
        auto_now=False,
        auto_now_add=False
    )
    reason = models.CharField(
        _("Reason"),
        max_length=50,
        choices=REASON_CHOICES,
        blank=True,
        null=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("User"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        """
        Meta configuration for the StockMovement model.
        """
        app_label = "inventory"
        db_table = "stock_movements"
        verbose_name = _("Stock Movement")
        verbose_name_plural = _("Stock Movements")

    def get_stock_movement_type_display(self):
        """
        Return the display value for the stock movement type.
        """
        return dict(self.STOCK_MOVEMENT_TYPE_CHOICES).get(self.stock_movement_type, "Unknown")

    def __str__(self):
        return f"{self.product} - {self.get_stock_movement_type_display()}"

    def get_absolute_url(self):
        """
        Return the URL to access a detail record for this stock movement.
        """
        return reverse("stockmovement_detail", kwargs={"pk": self.pk})
