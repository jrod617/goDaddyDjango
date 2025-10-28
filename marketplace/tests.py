"""Tests for the marketplace app."""
from __future__ import annotations

from django.test import TestCase
from django.urls import reverse

from .models import Brand, Shoe


class ShoeModelTests(TestCase):
    def setUp(self) -> None:
        self.brand = Brand.objects.create(name="Nike", slug="nike")

    def test_margin_calculates_percentage(self) -> None:
        shoe = Shoe.objects.create(
            brand=self.brand,
            name="Air Max 1",
            sku="AM1-001",
            size="10",
            condition=Shoe.Condition.NEW,
            asking_price=250,
            retail_price=200,
            seller_name="Taylor",
            seller_email="taylor@example.com",
        )
        self.assertAlmostEqual(shoe.margin, 25.0)

    def test_margin_zero_without_retail_price(self) -> None:
        shoe = Shoe.objects.create(
            brand=self.brand,
            name="Jordan 1",
            sku="AJ1-001",
            size="9",
            condition=Shoe.Condition.LIKE_NEW,
            asking_price=450,
            seller_name="Taylor",
            seller_email="taylor@example.com",
        )
        self.assertEqual(shoe.margin, 0.0)


class ShoeListViewTests(TestCase):
    def setUp(self) -> None:
        self.nike = Brand.objects.create(name="Nike", slug="nike")
        self.adidas = Brand.objects.create(name="Adidas", slug="adidas")
        Shoe.objects.create(
            brand=self.nike,
            name="Dunk Low Panda",
            sku="DUNK-001",
            size="8",
            condition=Shoe.Condition.GENTLY_USED,
            asking_price=220,
            retail_price=120,
            seller_name="Alex",
            seller_email="alex@example.com",
        )
        Shoe.objects.create(
            brand=self.adidas,
            name="Yeezy Boost 350",
            sku="YZY-350",
            size="9",
            condition=Shoe.Condition.NEW,
            asking_price=300,
            retail_price=220,
            is_published=False,
            seller_name="Jamie",
            seller_email="jamie@example.com",
        )

    def test_list_view_only_shows_published(self) -> None:
        url = reverse("marketplace:shoe-list")
        response = self.client.get(url)
        self.assertContains(response, "Dunk Low Panda")
        self.assertNotContains(response, "Yeezy Boost 350")

    def test_filter_by_brand(self) -> None:
        url = reverse("marketplace:shoe-list")
        response = self.client.get(url, {"brand": "nike"})
        self.assertContains(response, "Dunk Low Panda")
        self.assertNotContains(response, "Yeezy Boost 350")


class ShoeListingViewTests(TestCase):
    def setUp(self) -> None:
        self.brand = Brand.objects.create(name="Nike", slug="nike")

    def test_valid_form_creates_shoe(self) -> None:
        url = reverse("marketplace:listing-create")
        payload = {
            "brand": self.brand.pk,
            "name": "Jordan 4 Bred",
            "sku": "AJ4-BRED",
            "size": "10",
            "colorway": "Black/Red",
            "condition": Shoe.Condition.NEW,
            "description": "Classic colorway",
            "asking_price": 500,
            "retail_price": 225,
            "seller_name": "Chris",
            "seller_email": "chris@example.com",
            "seller_phone": "555-555-5555",
            "seller_notes": "Worn twice, includes box",
        }
        response = self.client.post(url, payload, follow=True)
        self.assertRedirects(response, reverse("marketplace:shoe-list"))
        self.assertTrue(Shoe.objects.filter(sku="AJ4-BRED").exists())

    def test_invalid_form_shows_errors(self) -> None:
        url = reverse("marketplace:listing-create")
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please correct the errors")
