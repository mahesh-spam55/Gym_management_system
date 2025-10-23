from django import forms
from .models import Trainer


class TrainerForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label="Trainer Name")

    class Meta:
        model = Trainer
        fields = [
            "employee_id",
            "name",
            "contact",
            "specialization",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-populate the combined name field when editing
        if self.instance and (self.instance.first_name or self.instance.last_name):
            full_name = f"{self.instance.first_name} {self.instance.last_name}".strip()
            self.fields["name"].initial = full_name

    def save(self, commit=True):
        # Split the combined name into first and last name
        name = self.cleaned_data.get("name", "").strip()
        first, *rest = name.split()
        self.instance.first_name = first if first else ""
        self.instance.last_name = " ".join(rest) if rest else ""
        return super().save(commit=commit)
