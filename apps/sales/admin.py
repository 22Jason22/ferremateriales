from django.contrib import admin
from .models import Quote, QuoteItem, Order, OrderItem

# Register your models here.
admin.site.register(Quote)
admin.site.register(QuoteItem)
admin.site.register(Order)
admin.site.register(OrderItem)
