from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.label
            })

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
