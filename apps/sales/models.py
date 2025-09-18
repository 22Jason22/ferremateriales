"""
Sales models.
"""
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from apps.crm.models import Customer
from apps.inventory.models import Product


class Quote(models.Model):
    """
    Model representing a sales quote.
    """
    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('sent', _('Sent')),
        ('accepted', _('Accepted')),
        ('rejected', _('Rejected')),
    ]

    customer = models.ForeignKey(
        Customer,
        verbose_name=_("Customer"),
        on_delete=models.CASCADE
    )
    quote_number = models.CharField(
        _("Quote Number"),
        max_length=50,
        unique=True
    )
    date = models.DateField(
        _("Date"),
        default=timezone.now
    )
    total_amount = models.DecimalField(
        _("Total Amount"),
        max_digits=10,
        decimal_places=2,
        default=0.00
    )
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    created_at = models.DateTimeField(
        _("Created At"),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _("Updated At"),
        auto_now=True
    )

    class Meta:
        """
        Meta configuration for the Quote model.
        """
        db_table = "sales_quotes"
        verbose_name = _("Sales Quote")
        verbose_name_plural = _("Sales Quotes")

    def __str__(self):
        return f"{self.quote_number} - {self.customer.name}"

    def get_absolute_url(self):
        """
        Return the URL to access a detail record for this quote.
        """
        return reverse("quote_detail", kwargs={"pk": self.pk})


class QuoteItem(models.Model):
    """
    Model representing an item in a sales quote.
    """
    quote = models.ForeignKey(
        Quote,
        verbose_name=_("Quote"),
        on_delete=models.CASCADE,
        related_name="items"
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
    price = models.DecimalField(
        _("Price"),
        max_digits=10,
        decimal_places=2
    )
    total = models.DecimalField(
        _("Total"),
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        """
        Meta configuration for the QuoteItem model.
        """
        db_table = "sales_quote_items"
        verbose_name = _("Sales Quote Item")
        verbose_name_plural = _("Sales Quote Items")

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"


class Order(models.Model):
    """
    Model representing a sales order.
    """
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('confirmed', _('Confirmed')),
        ('shipped', _('Shipped')),
        ('delivered', _('Delivered')),
        ('cancelled', _('Cancelled')),
    ]

    customer = models.ForeignKey(
        Customer,
        verbose_name=_("Customer"),
        on_delete=models.CASCADE
    )
    order_number = models.CharField(
        _("Order Number"),
        max_length=50,
        unique=True
    )
    date = models.DateField(
        _("Date"),
        default=timezone.now
    )
    total_amount = models.DecimalField(
        _("Total Amount"),
        max_digits=10,
        decimal_places=2,
        default=0.00
    )
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    quote = models.OneToOneField(
        Quote,
        verbose_name=_("Quote"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        _("Created At"),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _("Updated At"),
        auto_now=True
    )

    class Meta:
        """
        Meta configuration for the Order model.
        """
        db_table = "sales_orders"
        verbose_name = _("Sales Order")
        verbose_name_plural = _("Sales Orders")

    def __str__(self):
        return f"{self.order_number} - {self.customer.name}"

    def save(self, *args, **kwargs):
        """
        Override save method to update customer's last_purchase date.
        """
        super().save(*args, **kwargs)
        # Update customer's last_purchase with the order date
        if self.customer:
            # Convert date to datetime for last_purchase field
            order_datetime = timezone.datetime.combine(self.date, timezone.datetime.min.time())
            order_datetime = timezone.make_aware(order_datetime)
            self.customer.last_purchase = order_datetime
            self.customer.save(update_fields=['last_purchase'])

    def get_absolute_url(self):
        """
        Return the URL to access a detail record for this order.
        """
        return reverse("order_detail", kwargs={"pk": self.pk})


class OrderItem(models.Model):
    """
    Model representing an item in a sales order.
    """
    order = models.ForeignKey(
        Order,
        verbose_name=_("Order"),
        on_delete=models.CASCADE,
        related_name="items"
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
    price = models.DecimalField(
        _("Price"),
        max_digits=10,
        decimal_places=2
    )
    total = models.DecimalField(
        _("Total"),
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        """
        Meta configuration for the OrderItem model.
        """
        db_table = "sales_order_items"
        verbose_name = _("Sales Order Item")
        verbose_name_plural = _("Sales Order Items")

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
