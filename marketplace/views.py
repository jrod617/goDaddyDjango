"""Views for the sneaker marketplace."""
from __future__ import annotations
from typing import Any

from django.contrib import messages
from django.db.models import Count, Q
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import DetailView, ListView, TemplateView, FormView

from .forms import ShoeListingForm
from .models import Brand, Shoe


class ShoeListView(ListView):
    model = Shoe
    template_name = "marketplace/shoe_list.html"
    context_object_name = "shoes"
    paginate_by = 12

    def get_queryset(self):
        queryset = Shoe.objects.visible()
        filters = {
            "brand": self.request.GET.get("brand", "").strip(),
            "size": self.request.GET.get("size", "").strip(),
            "condition": self.request.GET.get("condition", "").strip(),
        }
        filters = {key: value for key, value in filters.items() if value}
        queryset = queryset.filter_for_filters(filters)
        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["brands"] = (
            Brand.objects.annotate(
                total=Count("shoes", filter=Q(shoes__is_published=True))
            ).order_by("name")
        )
        context["conditions"] = Shoe.Condition.choices
        context["active_filters"] = {
            key: value
            for key in ("brand", "size", "condition")
            if (value := self.request.GET.get(key))
        }
        return context


class ShoeDetailView(DetailView):
    model = Shoe
    template_name = "marketplace/shoe_detail.html"
    context_object_name = "shoe"


class ConsignmentLandingView(TemplateView):
    template_name = "marketplace/consignment_landing.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = ShoeListingForm()
        return context


class ShoeListingCreateView(FormView):
    template_name = "marketplace/listing_form.html"
    form_class = ShoeListingForm

    def get_success_url(self) -> str:
        return reverse("marketplace:shoe-list")

    def form_valid(self, form: ShoeListingForm) -> HttpResponse:
        form.save()
        messages.success(
            self.request,
            "Thanks! We've received your listing and will contact you shortly.",
        )
        return super().form_valid(form)

    def form_invalid(self, form: ShoeListingForm) -> HttpResponse:
        messages.error(
            self.request,
            "Please correct the errors below to submit your listing.",
        )
        return super().form_invalid(form)
