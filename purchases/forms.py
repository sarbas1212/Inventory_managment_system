from django import forms
from .models import Purchase, PurchaseItem
from vendors.models import Vendor
from products.models import Product

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ["vendor", "purchase_date", "discount_amount"]
        widgets = {
            "purchase_date": forms.DateInput(attrs={"type": "date"}),
        }


class PurchaseItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        fields = ["product", "quantity", "price", "tax_percentage"]
