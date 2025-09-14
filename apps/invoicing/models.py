"""zzz"""
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from apps.crm.models import Customer
from apps.sales.models import Order

class Invoice(models.Model):
    """
    Model representing an invoice.
    """

    STATUS_CHOICES = [
        (0, _("Draft")),
        (1, _("Sent")),
        (2, _("Paid")),
        (3, _("Overdue")),
    ]

    invoice_number = models.CharField(
        _("Invoice Number"),
        max_length=50,
    )
    date_issued = models.DateField(
        _("Date Issued"),
        auto_now=False,
        auto_now_add=False,
    )
    due_date = models.DateField(
        _("Due Date"),
        auto_now=False,
        auto_now_add=False,
    )
    customer = models.ForeignKey(
        "crm.Customer",
        verbose_name=_("Customer"),
        on_delete=models.CASCADE,
    )
    order = models.ForeignKey(
        "sales.Order",
        verbose_name=_("Sales Order"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    status = models.PositiveSmallIntegerField(
        _("Status"),
        choices=STATUS_CHOICES,
    )
    total_amount = models.DecimalField(
        _("Total Amount"),
        max_digits=10,
        decimal_places=2,
    )

    class Meta:
        """
        Meta configuration for the Invoice model.
        """
        db_table = "invoices"
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")

    def __str__(self):
        return str(self.invoice_number)

    def get_absolute_url(self):
        """
        Return the URL to access a detail record for this invoice.
        """
        return reverse("invoice_detail", kwargs={"pk": self.pk})


class Payment(models.Model):
    """
    Model representing a payment.
    """

    PAID_METHOD_CHOICES = [
        (0, _("Transfer")),
        (1, _("Card")),
        (2, _("Cash")),
    ]

    invoice = models.ForeignKey(
        Invoice,
        verbose_name=_("Invoice"),
        on_delete=models.CASCADE,
    )
    amount_paid = models.DecimalField(
        _("Amount Paid"),
        max_digits=10,
        decimal_places=2,
    )
    date_paid = models.DateField(
        _("Date Paid"),
        auto_now=False,
        auto_now_add=False,
    )
    paid_method = models.PositiveSmallIntegerField(
        _("Paid Method"),
        choices=PAID_METHOD_CHOICES,
    )

    class Meta:
        """
        Meta configuration for the Payment model.
        """
        db_table = "payments"
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")

    def __str__(self):
        """
        Returns the string representation of the Payment.
        """
        return str(self.invoice)

    def get_absolute_url(self):
        """
        Return the URL to access a detail record for this payment.
        """
        return reverse("payment_detail", kwargs={"pk": self.pk})
