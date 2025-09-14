from django.contrib import admin
from .models import Customer, Supplier, Lead

# Register your models here.
admin.site.register(Customer)
admin.site.register(Supplier)
admin.site.register(Lead)