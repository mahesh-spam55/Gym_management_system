from django import forms
from .models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [
            "paid_on",
            "member",
            "amount",
            "transaction_type",
            "membership_type",
        ]
        widgets = {
            "paid_on": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "member": forms.Select(attrs={"class": "form-select"}),
            "amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
            "transaction_type": forms.Select(attrs={"class": "form-select"}),
            "membership_type": forms.Select(attrs={"class": "form-select"}),
        }
