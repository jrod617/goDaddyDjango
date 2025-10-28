"""Admin configuration for marketplace models."""
from __future__ import annotations

from django.contrib import admin

from .models import Brand, Shoe


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Shoe)
class ShoeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "brand",
        "size",
        "condition",
        "asking_price",
        "is_published",
        "seller_name",
    )
    list_filter = ("brand", "condition", "is_published")
    search_fields = ("name", "sku", "brand__name", "seller_name")
    list_editable = ("asking_price", "is_published")
    autocomplete_fields = ("brand",)
    ordering = ("-created_at",)
