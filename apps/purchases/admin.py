from django.contrib import admin
from .models import PurchaseOrder, PurchaseOrderItem, GoodsReceipt, GoodsReceiptItem

# Register your models here.
admin.site.register(PurchaseOrder)
admin.site.register(PurchaseOrderItem)
admin.site.register(GoodsReceipt)
admin.site.register(GoodsReceiptItem)
