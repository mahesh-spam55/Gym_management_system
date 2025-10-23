from django import forms
from .models import Member


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
            "member_id",
            "name",
            "contact",
            "address",
            "date_of_joining",
        ]
        widgets = {
            "date_of_joining": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }
