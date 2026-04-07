# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Django bookmark manager with two apps:
- **`api`** — Django REST Framework API for bookmarks and tags
- **`webpage`** — Server-rendered HTML frontend for browsing bookmarks

Database: MySQL (`bookmark_v2` on 127.0.0.1:3306). All models use `managed = False` — schema changes must be applied directly in MySQL, never via Django migrations.

## Commands

```bash
# Activate virtual environment (Windows)
venv\Scripts\activate

# Run development server
python manage.py runserver

# Run all tests
python manage.py test

# Run tests for a specific app
python manage.py test api
python manage.py test webpage

# Apply migrations (for Django-managed models only, e.g. auth, sessions)
python manage.py migrate
```

## Architecture

### URL Routing
- `/` → `webpage.views.index` — paginated bookmark list with filtering
- `/<pk>/visit/` → `webpage.views.bookmark_visit` — increments `visit_count` and redirects to the URL
- `/api/` → DRF router with `BookmarkViewSet` and `TagViewSet`
- `/admin/` → Django admin

### Data Model
Five tables in `api/models.py` (all `managed = False`):
- `Bookmarks` — core bookmark data; fields include `is_domestic`, `site_scale`, `is_active`, `is_favorite`, `visit_count`
- `Tags` — name/slug/color
- `BookmarkTags` — M2M join table with `CompositePrimaryKey('bookmark_id', 'tag_id')`
- `UserBookmarks` — maps users → bookmarks (surrogate `id` PK, unique on `user_id+bookmark_id`)
- `UserTags` — maps users → tags (surrogate `id` PK, unique on `user_id+tag_id`)

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

### Admin (`api/admin.py`)
`UserBookmarksAdmin` and `UserTagsAdmin` are registered, allowing manual management of user–bookmark and user–tag associations. Admin does not support models with `CompositePrimaryKey` — use a surrogate `id` for any new join tables intended to appear in admin.
