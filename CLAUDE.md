# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Django bookmark manager with three apps:
- **`api`** — Django REST Framework API for bookmarks and tags
- **`webpage`** — Server-rendered HTML frontend for browsing bookmarks
- **`payment`** — Alipay-based paid registration flow (¥5.00 one-time fee)

Database: MySQL (`bookmark_v2` on 127.0.0.1:3306). All models use `managed = False` — schema changes must be applied directly in MySQL, never via Django migrations.

## Environment Setup

Settings are loaded from `.env` in the project root. Required variables:

```
SECRET_KEY=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=127.0.0.1   # optional, default 127.0.0.1
DB_PORT=3306         # optional, default 3306
DEBUG=True           # optional, default False
ALLOWED_HOSTS=       # optional, comma-separated extra hosts
```

## Infrastructure

### Reverse Proxy
- **Caddy** runs as a Docker container for reverse proxying
- Caddyfile is mounted at `/root/caddy/Caddyfile`
- Static files are served directly by Caddy from `/root/bookmark/staticfiles`
- Note: `/root` requires `o+x` permission so the Caddy container can traverse into subdirectories

### Application Server
- **Gunicorn** runs via `bookmark.service` (systemd), binding to `0.0.0.0:8000`

## Commands

```bash
# Activate virtual environment
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# Run development server
python manage.py runserver

# Run tests
python manage.py test           # all
python manage.py test api       # single app

# Apply migrations (for Django-managed models only, e.g. auth, sessions)
python manage.py migrate

# Collect static files (production)
python manage.py collectstatic
```

## Architecture

### URL Routing
- `/` → `webpage.views.index` — paginated bookmark list with filtering
- `/<pk>/visit/` → `webpage.views.bookmark_visit` — increments `visit_count` and redirects to the URL
- `/api/` → DRF router with `BookmarkViewSet` and `TagViewSet`
- `/payment/register/` → registration info page with payment CTA
- `/payment/create-order/` → creates `PaymentOrder` and redirects to Alipay gateway
- `/payment/return/` → sync callback; verifies signature, marks order `paid`
- `/payment/notify/` → async callback (CSRF-exempt); marks order `paid`
- `/payment/do-register/` → validates form, creates `User`, marks order `registered`, logs in
- `/accounts/login/` → Django built-in `LoginView` with template `registration/login.html`
- `/admin/` → Django admin

### Authentication
All `webpage` views use `@login_required` (redirects to `/accounts/login/`). The DRF API uses `SessionAuthentication` + `IsAuthenticated` — all API endpoints also require login.

### Data Model
Six tables, all `managed = False`:
- `api/models.py`: `Bookmarks`, `Tags`, `BookmarkTags` (composite PK), `UserBookmarks`, `UserTags`
- `payment/models.py`: `PaymentOrder` — columns `out_trade_no`, `trade_no`, `amount`, `status` (`pending`→`paid`→`registered`), `created_at`, `paid_at`

MySQL DDL for `PaymentOrder` is in the model's docstring.

The `webpage` app has its own `models.py` but it is empty — it imports all models from `api.models`.

### Per-User Data Isolation
Every view and viewset filters data by the authenticated user via `UserBookmarks` and `UserTags`. Superusers bypass all filters and see everything. "Deleting" a bookmark or tag only removes the `UserBookmarks`/`UserTags` association — the underlying record is never deleted.

- **API**: `BookmarkViewSet` and `TagViewSet` filter `get_queryset()` by `userbookmarks__user` / `usertags__user`. `perform_create` inserts the association row after saving. `destroy` removes only the association row.
- **Frontend**: `webpage/views.index` applies the same queryset filter; `bookmark_visit` returns 404 if the user has no association with the requested bookmark.

### API Layer (`api/`)
`BookmarkViewSet` supports filtering via query params: `?favorite=1`, `?is_active=0|1`, `?tag=<slug>`, `?keyword=<text>`, `?search_in=title|description|all`.

`BookmarkSerializer` exposes a read-only `tags` field (nested `TagSerializer`) and a write-only `tag_ids` field. On `update`, `tag_ids` must be present — passing it replaces all existing tag associations via `BookmarkTags`.

DRF is configured with `SessionAuthentication` and `IsAuthenticated` globally (see `REST_FRAMEWORK` in `settings.py`).

### Frontend Layer (`webpage/`)
`webpage/views.index` mirrors the API filtering logic and renders `webpage/templates/webpage/index.html` with pagination (default 21 per page, capped 3–60). The tag sidebar (`all_tags`) is also filtered by the current user.

### Payment Layer (`payment/`)
Uses the `python-alipay-sdk` (`alipay` package). Config is read from `settings.ALIPAY_CONFIG` which is populated from environment variables. The `_get_alipay()` helper in `payment/views.py` wraps the bare key strings with PEM headers before passing to the SDK.

Session key `pending_out_trade_no` tracks the in-flight order across the redirect loop. The `register_info` view checks this key to show appropriate state (no order / waiting for notify / already paid).

### Admin (`api/admin.py`)
`UserBookmarksAdmin` and `UserTagsAdmin` are registered, allowing manual management of user–bookmark and user–tag associations. Admin does not support models with `CompositePrimaryKey` — use a surrogate `id` for any new join tables intended to appear in admin.
