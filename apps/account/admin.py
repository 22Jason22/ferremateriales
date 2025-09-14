from django.contrib import admin
from .models import Account, Transaction, TransactionEntry

# Register your models here.
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(TransactionEntry)