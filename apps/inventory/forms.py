"""zzz"""
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    """zzz"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.label
            })

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
