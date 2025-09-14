"""zzz"""
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    """zzz"""
    class Meta:
        """zzz"""
        model = Product
        fields = [
            'name',
            'category',
            'price',
            'unit',
            'description',
            'discount_percent',
            'is_new',
            'current_stock',
            'image'
        ]
