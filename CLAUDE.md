# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Django bookmark manager with two apps:
- **`api`** — Django REST Framework API for bookmarks and tags
- **`webpage`** — Server-rendered HTML frontend for browsing bookmarks

Database: MySQL (`bookmark_v2` on 127.0.0.1:3306). The models use `managed = False`, meaning Django does not manage table migrations — schema changes must be applied to the database directly.

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

# Apply migrations (for Django-managed models only)
python manage.py migrate
```

## Architecture

### URL Routing
- `/` → `webpage.views.index` — paginated bookmark list with filtering
- `/<pk>/visit/` → `webpage.views.bookmark_visit` — increments `visit_count` and redirects to the URL
- `/api/` → DRF router with `BookmarkViewSet` and `TagViewSet`
- `/admin/` → Django admin

### Data Model
Three tables (all `managed = False`):
- `Bookmarks` — core bookmark data; fields include `is_domestic`, `site_scale`, `is_active`, `is_favorite`, `visit_count`
- `Tags` — name/slug/color
- `BookmarkTags` — M2M join table with a `CompositePrimaryKey('bookmark_id', 'tag_id')`

### API Layer (`api/`)
`BookmarkViewSet` supports filtering via query params: `?favorite=1`, `?is_active=0|1`, `?tag=<slug>`, `?keyword=<text>`, `?search_in=title|description|all`.

`BookmarkSerializer` exposes a read-only `tags` field (nested `TagSerializer`) and a write-only `tag_ids` field. On `update`, `tag_ids` must be present (not optional) — passing it replaces all existing tag associations via `BookmarkTags`.

### Frontend Layer (`webpage/`)
`webpage/views.index` mirrors the API filtering logic but renders `webpage/templates/webpage/index.html` with pagination (default 15 per page, capped 3–60).
