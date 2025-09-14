"""
Purchases models.
"""
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings

from apps.crm.models import Supplier
from apps.inventory.models import Product


class PurchaseOrder(models.Model):
    """
    Model representing a purchase order.
    """
    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('sent', _('Sent')),
        ('confirmed', _('Confirmed')),
        ('received', _('Received')),
        ('cancelled', _('Cancelled')),
    ]

    supplier = models.ForeignKey(
        Supplier,
        verbose_name=_("Supplier"),
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
        Meta configuration for the PurchaseOrder model.
        """
        db_table = "purchase_orders"
        verbose_name = _("Purchase Order")
        verbose_name_plural = _("Purchase Orders")

    def __str__(self):
        return f"{self.order_number} - {self.supplier.name}"

    def get_absolute_url(self):
        """
        Return the URL to access a detail record for this purchase order.
        """
        return reverse("purchase_order_detail", kwargs={"pk": self.pk})


class PurchaseOrderItem(models.Model):
    """
    Model representing an item in a purchase order.
    """
    purchase_order = models.ForeignKey(
        PurchaseOrder,
        verbose_name=_("Purchase Order"),
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
        Meta configuration for the PurchaseOrderItem model.
        """
        db_table = "purchase_order_items"
        verbose_name = _("Purchase Order Item")
        verbose_name_plural = _("Purchase Order Items")

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"


class GoodsReceipt(models.Model):
    """
    Model representing a goods receipt.
    """
    purchase_order = models.ForeignKey(
        PurchaseOrder,
        verbose_name=_("Purchase Order"),
        on_delete=models.CASCADE
    )
    receipt_number = models.CharField(
        _("Receipt Number"),
        max_length=50,
        unique=True
    )
    date = models.DateField(
        _("Date"),
        default=timezone.now
    )
    received_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Received By"),
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
        Meta configuration for the GoodsReceipt model.
        """
        db_table = "goods_receipts"
        verbose_name = _("Goods Receipt")
        verbose_name_plural = _("Goods Receipts")

    def __str__(self):
        return f"{self.receipt_number} - {self.purchase_order.order_number}"

    def get_absolute_url(self):
        """
        Return the URL to access a detail record for this goods receipt.
        """
        return reverse("goods_receipt_detail", kwargs={"pk": self.pk})


class GoodsReceiptItem(models.Model):
    """
    Model representing an item in a goods receipt.
    """
    goods_receipt = models.ForeignKey(
        GoodsReceipt,
        verbose_name=_("Goods Receipt"),
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        Product,
        verbose_name=_("Product"),
        on_delete=models.CASCADE
    )
    quantity_received = models.DecimalField(
        _("Quantity Received"),
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        """
        Meta configuration for the GoodsReceiptItem model.
        """
        db_table = "goods_receipt_items"
        verbose_name = _("Goods Receipt Item")
        verbose_name_plural = _("Goods Receipt Items")

    def __str__(self):
        return f"{self.product.name} ({self.quantity_received})"