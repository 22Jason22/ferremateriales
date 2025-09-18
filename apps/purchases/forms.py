from django import forms
from .models import PurchaseOrder

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['supplier', 'order_number', 'date', 'total_amount', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
