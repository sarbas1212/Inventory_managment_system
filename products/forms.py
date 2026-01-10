from django import forms
from .models import Product,Category

class ProductForm(forms.ModelForm):
    opening_stock = forms.DecimalField(
        required=False,
        min_value=0,
        label="Opening Stock",
        help_text="Optional. Initial stock quantity",
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Product
        fields = [
            "name", "sku", "barcode", "category",
            "purchase_price", "selling_price", "tax_percentage",
            "unit", "reorder_level"
        ]

    def clean_sku(self):
        sku = self.cleaned_data.get("sku")
        qs = Product.objects.filter(sku=sku, is_active=True)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("A product with this SKU already exists.")
        return sku

    def clean_name(self):
        name = self.cleaned_data.get("name")
        qs = Product.objects.filter(name__iexact=name, is_active=True)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("A product with this name already exists.")
        return name



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "parent"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        qs = Category.objects.filter(name__iexact=name, is_active=True)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("A category with this name already exists.")
        return name