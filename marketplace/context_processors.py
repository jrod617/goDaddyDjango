"""Extra template context for the marketplace."""
from __future__ import annotations

from django.conf import settings


def site_brand(request):
    """Expose the configured marketplace brand name to templates."""

    return {"site_brand": getattr(settings, "SITE_BRAND", "SoleSwap")}
