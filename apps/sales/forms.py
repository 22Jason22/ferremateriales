from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'customer',
            'order_number',
            'date',
            'total_amount',
            'status',
            'quote',
        ]
