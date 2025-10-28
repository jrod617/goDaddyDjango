"""Forms for interacting with sneaker listings."""
from __future__ import annotations

from django import forms

from .models import Brand, Shoe


class ShoeListingForm(forms.ModelForm):
    """Collects the minimum info to create a new listing."""

    seller_name = forms.CharField(max_length=120, help_text="Your full name")
    seller_email = forms.EmailField(help_text="Where we can reach you about the listing")
    seller_phone = forms.CharField(
        max_length=20,
        required=False,
        help_text="Optional: add a phone number for faster communication",
    )

    class Meta:
        model = Shoe
        fields = [
            "brand",
            "name",
            "sku",
            "size",
            "colorway",
            "condition",
            "description",
            "seller_name",
            "seller_email",
            "seller_phone",
            "seller_notes",
            "asking_price",
            "retail_price",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "seller_notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["brand"].queryset = Brand.objects.order_by("name")
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
