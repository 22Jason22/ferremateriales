from django import forms
from .models import Customer, Supplier

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'name',
            'tax_id',
            'client_type',
            'phone',
            'contact_name',
            'email',
            'address',
            'status',
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2}),
        }

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = [
            'razon_social',
            'ruc',
            'rubro',
            'telefono',
            'contacto_nombre',
            'contacto_email',
            'contacto_telefono',
            'direccion',
            'plazo_pago',
            'estado',
            'certificado',
        ]
        widgets = {
            'direccion': forms.Textarea(attrs={'rows': 2}),
        }
