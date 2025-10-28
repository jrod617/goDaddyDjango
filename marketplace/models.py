"""Database models for the marketplace domain."""
from __future__ import annotations

from django.db import models
from django.urls import reverse


class Brand(models.Model):
    """Represents the manufacturer of a sneaker."""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:  # pragma: no cover - simple display
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("marketplace:shoe-list") + f"?brand={self.slug}"


class ShoeQuerySet(models.QuerySet):
    def published(self) -> "ShoeQuerySet":
        return self.filter(is_published=True)

    def visible(self) -> "ShoeQuerySet":
        return self.published().select_related("brand")

    def filter_for_filters(self, filters: dict[str, str]) -> "ShoeQuerySet":
        queryset: ShoeQuerySet = self
        if brand := filters.get("brand"):
            queryset = queryset.filter(brand__slug=brand)
        if size := filters.get("size"):
            queryset = queryset.filter(size=size)
        if condition := filters.get("condition"):
            queryset = queryset.filter(condition=condition)
        return queryset


class Shoe(models.Model):
    """Represents a sneaker listing available for resale."""

    class Condition(models.TextChoices):
        NEW = "new", "New"
        LIKE_NEW = "like_new", "Like New"
        GENTLY_USED = "gently_used", "Gently Used"
        USED = "used", "Used"

    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name="shoes")
    name = models.CharField(max_length=120)
    sku = models.CharField("SKU", max_length=50, unique=True)
    size = models.CharField(max_length=10)
    colorway = models.CharField(max_length=100, blank=True)
    condition = models.CharField(
        max_length=20,
        choices=Condition.choices,
        default=Condition.LIKE_NEW,
    )
    description = models.TextField(blank=True)
    seller_name = models.CharField(max_length=120)
    seller_email = models.EmailField()
    seller_phone = models.CharField(max_length=20, blank=True)
    seller_notes = models.TextField(blank=True)
    asking_price = models.DecimalField(max_digits=8, decimal_places=2)
    retail_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ShoeQuerySet.as_manager()

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("brand", "name", "size", "condition")

    def __str__(self) -> str:  # pragma: no cover - simple display
        return f"{self.brand.name} {self.name} ({self.size})"

    def get_absolute_url(self) -> str:
        return reverse("marketplace:shoe-detail", args=[self.pk])

    @property
    def margin(self) -> float:
        """Percentage markup over retail price, if retail price is provided."""

        if not self.retail_price:
            return 0.0
        return float((self.asking_price - self.retail_price) / self.retail_price * 100)
