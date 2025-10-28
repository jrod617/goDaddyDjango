"""URL routing for the marketplace app."""
from django.urls import path

from .views import (
    ConsignmentLandingView,
    ShoeDetailView,
    ShoeListView,
    ShoeListingCreateView,
)

app_name = "marketplace"

urlpatterns = [
    path("", ShoeListView.as_view(), name="shoe-list"),
    path("listings/new/", ShoeListingCreateView.as_view(), name="listing-create"),
    path("consign/", ConsignmentLandingView.as_view(), name="consignment"),
    path("shoes/<int:pk>/", ShoeDetailView.as_view(), name="shoe-detail"),
]
