from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            "name",
            "phone",
            "email",
            "gst_number",
            "billing_address",
            "shipping_address",
            "credit_limit",
        ]

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")

        qs = Customer.objects.filter(
            phone=phone,
            is_active=True
        )

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError(
                "A customer with this phone number already exists."
            )

        return phone

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if not email:
            return email

        qs = Customer.objects.filter(
            email=email,
            is_active=True
        )

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError(
                "A customer with this email already exists."
            )

        return email
