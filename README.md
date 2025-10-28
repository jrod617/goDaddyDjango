# SoleSwap Marketplace

SoleSwap is a Django-powered marketplace that helps you manage a curated inventory of resale sneakers, track consignor information, and collect new listings from sellers.

## Features

- **Inventory management** – Manage sneaker listings with brand, size, condition, pricing, and seller contact fields.
- **Filtering** – Browse the catalog by brand, size, or condition from the storefront landing page.
- **Consignment intake** – Collect leads via a simple form that stores seller contact info alongside the listing.
- **Admin ready** – Pre-configured Django admin for quickly curating inventory.

## Getting Started

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Apply database migrations**

   ```bash
   python manage.py migrate
   ```

3. **Create a superuser (optional but recommended)**

   ```bash
   python manage.py createsuperuser
   ```

4. **Run the development server**

   ```bash
   python manage.py runserver
   ```

5. Open http://127.0.0.1:8000/ to explore the storefront and http://127.0.0.1:8000/admin/ to manage inventory.

## Running Tests

```bash
python manage.py test
```

## Configuration

You can customize a few environment variables to tailor the deployment:

- `DJANGO_SECRET_KEY` – Override the default development secret.
- `DJANGO_DEBUG` – Set to `False` in production.
- `DJANGO_ALLOWED_HOSTS` – Comma separated list of hosts allowed to serve the site.
- `SITE_BRAND` – Brand name rendered across templates (defaults to `SoleSwap`).

## Project Layout

- `shoe_resale/` – Django project configuration (settings, URL routing, WSGI/ASGI).
- `marketplace/` – Core resale app with models, forms, views, URLs, and tests.
- `templates/` – HTML templates for the storefront and consignment funnel.
- `static/` – Global stylesheet used by the public-facing pages.

## License

This project is licensed under the terms of the MIT license. See [LICENSE](LICENSE) for details.
