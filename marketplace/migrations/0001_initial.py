# Generated manually for initial marketplace schema
from __future__ import annotations

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Brand",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
                ("slug", models.SlugField(max_length=120, unique=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Shoe",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("sku", models.CharField(max_length=50, unique=True, verbose_name="SKU")),
                ("size", models.CharField(max_length=10)),
                ("colorway", models.CharField(blank=True, max_length=100)),
                (
                    "condition",
                    models.CharField(
                        choices=[
                            ("new", "New"),
                            ("like_new", "Like New"),
                            ("gently_used", "Gently Used"),
                            ("used", "Used"),
                        ],
                        default="like_new",
                        max_length=20,
                    ),
                ),
                ("description", models.TextField(blank=True)),
                ("seller_name", models.CharField(max_length=120)),
                ("seller_email", models.EmailField(max_length=254)),
                ("seller_phone", models.CharField(blank=True, max_length=20)),
                ("seller_notes", models.TextField(blank=True)),
                ("asking_price", models.DecimalField(decimal_places=2, max_digits=8)),
                (
                    "retail_price",
                    models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
                ),
                ("is_published", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "brand",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="shoes",
                        to="marketplace.brand",
                    ),
                ),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.AlterUniqueTogether(name="shoe", unique_together={("brand", "name", "size", "condition")}),
    ]
