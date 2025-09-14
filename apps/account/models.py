"""Core models for the Nexus project."""
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator


class Account(models.Model):
    """
    Model representing an Account.
    """
    name = models.CharField(
        _("Name"),
        max_length=255,
    )
    account_number = models.CharField(
        _("Account Number"),
        max_length=50,
        unique=True)
    balance = models.DecimalField(
        _("Balance"),
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        """Meta class for the account model."""
        db_table = "accounts"
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")

    def __str__(self):
        return f"{self.name} ({self.account_number})"

    def get_absolute_url(self):
        """
        Returns the URL to access a detail record for this account.
        """
        return reverse("account_detail", kwargs={"pk": self.pk})


class Transaction(models.Model):
    """
    Model representing a Transaction.
    """
    TRANSACTION_TYPE_CHOICES = [
        ("debit", _("Debit")),
        ("credit", _("Credit")),
    ]

    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="transactions")
    transaction_date = models.DateTimeField(_("Transaction Date"))
    description = models.CharField(
        _("Description"), max_length=255, blank=True)
    amount = models.DecimalField(
        _("Amount"),
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )
    transaction_type = models.CharField(
        _("Transaction Type"),
        max_length=6,
        choices=TRANSACTION_TYPE_CHOICES,
    )

    class Meta:
        """Meta class for the transaction model."""
        db_table = "transactions"
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")

    def __str__(self):
        transaction_type = self.transaction_type if isinstance(
            self.transaction_type, str) else str(self.transaction_type)
        transaction_date = self.transaction_date.strftime(
            '%Y-%m-%d') if hasattr(self.transaction_date, 'strftime') else str(self.transaction_date)
        return (
            f"{transaction_type.title()} - {self.amount} "
            f"on "
            f"{transaction_date}"
        )

    def get_absolute_url(self):
        """
        Returns the URL to access a detail record for this transaction.
        """
        return reverse("transaction_detail", kwargs={"pk": self.pk})


class TransactionEntry(models.Model):
    """
    Model representing a Transaction Entry.
    """
    transaction = models.ForeignKey(
        Transaction, on_delete=models.CASCADE, related_name="entries")
    entry_date = models.DateTimeField(_("Entry Date"))
    amount = models.DecimalField(_("Amount"), max_digits=12, decimal_places=2)
    description = models.CharField(
        _("Description"), max_length=255, blank=True)

    class Meta:
        """Meta class for the transaction entry model."""
        db_table = "transaction_entries"
        verbose_name = _("Transaction Entry")
        verbose_name_plural = _("Transaction Entries")

    def __str__(self):
        entry_date = self.entry_date.strftime(
            '%Y-%m-%d') if hasattr(self.entry_date, 'strftime') else str(self.entry_date)
        return (
            f"Entry of {self.amount} "
            f"on {entry_date}"
        )
