from django import forms
from .models import Vendor

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        # Only include fields that user can edit
        fields = [
            "name",
            "phone",
            "email",
            "gst_number",
            "address",
            "outstanding_balance",
        ]
        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
        }
