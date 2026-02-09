# payments/forms.py
from django import forms
from .models import Payment

class VendorPaymentForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2)
    payment_method = forms.ChoiceField(choices=Payment.PAYMENT_METHODS)
    transaction_id = forms.CharField(required=False)
    payment_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"})
    )

class CustomerPaymentForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2)
    payment_method = forms.ChoiceField(choices=Payment.PAYMENT_METHODS)
    transaction_id = forms.CharField(required=False)
    payment_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"})
    )
