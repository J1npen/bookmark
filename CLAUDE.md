# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A bookmark manager with a Django REST API backend and a Vue 3 SPA frontend:
- **`backend/api`** — DRF API for bookmarks and tags
- **`backend/webpage`** — Legacy server-rendered HTML frontend (still in use)
- **`backend/payment`** — Alipay-based paid registration flow (¥5.00 one-time fee)
- **`frontend/`** — Vue 3 SPA (Vite + Pinia + Vue Router + Axios)

Database: MySQL (`bookmark_v2` on 127.0.0.1:3306). All models use `managed = False` — schema changes must be applied directly in MySQL, never via Django migrations.

## Environment Setup

`.env` lives at the **repo root** and is loaded by both the backend and any tooling. Required variables:

```
SECRET_KEY=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=127.0.0.1       # optional, default 127.0.0.1
DB_PORT=3306             # optional, default 3306
DEBUG=True               # optional, default False
ALLOWED_HOSTS=           # optional, comma-separated extra hosts
OPENAI_API_KEY=          # used by /api/describe/ for AI bookmark descriptions
OPENAI_BASE_URL=         # optional, defaults to https://api.openai.com
ALIPAY_APP_ID=
ALIPAY_PRIVATE_KEY=
ALIPAY_PUBLIC_KEY=
ALIPAY_SANDBOX=True
```

## Commands

```bash
# ── Backend (run from backend/) ──
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows

python manage.py runserver    # dev server on :8000
python manage.py test         # all tests
python manage.py test api     # single app
python manage.py migrate      # Django-managed tables only (auth, sessions)
python manage.py collectstatic

# ── Frontend (run from frontend/) ──
npm install
npm run dev      # Vite dev server on :5173, proxies /api and /accounts → :8000
npm run build    # outputs to frontend/dist/
```

## Infrastructure

- **Caddy** (Docker) reverse-proxies traffic; Caddyfile at `/root/caddy/Caddyfile`; static files served from `/root/bookmark/staticfiles`. `/root` requires `o+x` so the container can traverse it.
- **Gunicorn** runs via `bookmark.service` (systemd) on `0.0.0.0:8000`

## Architecture

### URL Routing (Django)
- `/` → `webpage.views.index` — paginated bookmark list with filtering
- `/<pk>/visit/` → `webpage.views.bookmark_visit` — increments `visit_count`, redirects
- `/api/bookmarks/` → `BookmarkViewSet` (CRUD + `?tag=`, `?keyword=`, `?search_in=`, `?page=`, `?page_size=`)
- `/api/bookmarks/<id>/visit/` → POST, increments `visit_count`
- `/api/tags/` → `TagViewSet` (CRUD)
- `/api/fetch-url-meta/` → GET, scrapes title + favicon from a URL
- `/api/describe/` → GET, uses GPT-4o-mini to generate a one-sentence bookmark description
- `/payment/register/` → registration info page with payment CTA
- `/payment/create-order/` → creates `PaymentOrder`, redirects to Alipay gateway
- `/payment/return/` → sync callback; verifies signature, marks order `paid`
- `/payment/notify/` → async callback (CSRF-exempt); marks order `paid`
- `/payment/do-register/` → validates form, creates `User`, marks order `registered`, logs in
- `/accounts/login/` → Django `LoginView`
- `/admin/` → Django admin

### Authentication
All `webpage` views use `@login_required`. DRF uses `SessionAuthentication` + `IsAuthenticated` globally — all API endpoints require login.

The Vue frontend authenticates by POSTing to `/accounts/login/` (form-encoded) after priming a CSRF cookie via `GET /api/`. Subsequent requests include `X-CSRFToken` from the cookie for mutating methods. Auth state is detected by probing `GET /api/bookmarks/` — 401/403 redirects to `/login`.

### Data Model
Six tables, all `managed = False`:
- `api/models.py`: `Bookmarks`, `Tags`, `BookmarkTags` (composite PK), `UserBookmarks`, `UserTags`
- `payment/models.py`: `PaymentOrder` — status flow: `pending` → `paid` → `registered`

MySQL DDL for `PaymentOrder` is in the model's docstring.

### Per-User Data Isolation
Every view/viewset filters by the authenticated user via `UserBookmarks` and `UserTags`. Superusers bypass filters. "Deleting" a bookmark or tag only removes the association row — the underlying record is never deleted.

### Vue 3 Frontend (`frontend/src/`)
- **`router/index.js`** — two routes: `/login` (public) and `/` (requires auth). Navigation guard calls `auth.check()` on first load.
- **`stores/auth.js`** — Pinia store; persists username in `localStorage` (`bm_username`). `check()` probes `/api/bookmarks/` to verify session.
- **`stores/bookmarks.js`** — holds `items`, `total`, `page`, `pageSize` (persisted in `localStorage` as `bm_pageSize`), `activeTag`, `keyword`.
- **`stores/tags.js`** — loads and caches the tag list.
- **`api/http.js`** — Axios instance with `baseURL: '/'`, `withCredentials: true`, CSRF injection, and 401/403 → `/login` redirect.
- **`api/index.js`** — thin wrappers around all API calls.
- **`views/HomeView.vue`** — single-page UI: sidebar (tag nav + user menu), search bar, bookmark grid, pagination, settings modal, add-bookmark modal with auto-fetch.

### Payment Layer (`payment/`)
Uses `python-alipay-sdk`. `_get_alipay()` wraps bare key strings with PEM headers. Session key `pending_out_trade_no` tracks the in-flight order across the redirect loop.

### Admin (`api/admin.py`)
`UserBookmarksAdmin` and `UserTagsAdmin` allow manual association management. Admin does not support `CompositePrimaryKey` — use a surrogate `id` for any new join tables intended to appear in admin.

使用中文回复。
