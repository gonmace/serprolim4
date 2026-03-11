# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Django + Wagtail CMS project for a septic tank cleaning service (limpiezapozossepticos.com). Multi-country landing page system with blog, SEO, tracking, and WhatsApp chat integration.

## Commands

All commands assume the dev settings unless otherwise noted. The `manage.py` defaults to `core.dev`.

```bash
# Development server
python manage.py runserver

# Migrations
python manage.py migrate
python manage.py makemigrations

# Tests (only chat/tests.py exists)
python manage.py test

# Tailwind CSS (must rebuild after CSS changes)
python manage.py tailwind build
python manage.py tailwind start   # watch mode

# Django shell
python manage.py shell_plus       # uses django-extensions

# Production commands (use --settings=core.prod)
python manage.py collectstatic --settings=core.prod
```

## Settings Structure

- `core/settings.py` — shared base settings
- `core/dev.py` — extends base; DEBUG=True, console email, browser-reload, Tailwind
- `core/prod.py` — extends base; file-based cache, gunicorn, reads `.env`

`manage.py` defaults to `core.dev`. `wsgi.py` and `entrypoint.sh` use `core.prod`.

## Architecture

### Apps

| App | Role |
|-----|------|
| `home` | Landing pages per country (LandingPage, LandingService, LandingFAQ) |
| `blog` | Wagtail blog (BlogPage, BlogIndexPage, BaseStreamBlock, templatetags) |
| `config` | CountrySettings, GeneralSettings, MetadataPageMixin, CountryMiddleware, context processors |
| `tracking` | TrackingSettings singleton — raw HTML/JS snippets injected into all templates |
| `chat` | WhatsApp proxy API at `/chat/api/send/` (forwards to n8n webhook) |
| `theme` | Tailwind CSS v4 + DaisyUI v5 config and build |

### Multi-Country Landing Pages

`LandingPage` (in `home/`) is a plain Django model (not Wagtail). Fallback chain: requested country → Bolivia default → first enabled → first available. Each country is a `CountrySettings` instance; `CountryMiddleware` auto-detects from `?country=XX` query param or session and attaches to `request.country`.

### Config App

Central app merging country/general settings, SEO, and metadata:
- `CountrySettings` — per-country config (contact info, theme, social links). Table: `wgeneraldata_countrysettings`
- `GeneralSettings` — global singleton fallback. Table: `wgeneraldata_generalsettings`
- `MetadataPageMixin` — abstract Wagtail mixin adding `search_image` and promote panels to blog pages
- `CountryMiddleware` — attaches `request.country` on every request
- `context_processors.site_settings` — injects `{{ site_settings }}` (current CountrySettings)

### Tracking

`TrackingSettings` singleton (table: `wanalytics_analyticssettings`) stores full HTML/JS snippets:
- `gtm`, `google_analytics`, `google_ads`, `adsense`, `fb_pixel`, `open_graph`
- `head_scripts`, `body_scripts` — custom injections
- Injected via `tracking.context_processors.project_analytics` as `{{ project_analytics }}`
- Templates use `{{ project_analytics.gtm|safe }}` etc. — paste the full snippet, no ID substitution

### SEO System

- `config.metadata.MetadataPageMixin` adds `search_image` and promote panels to Wagtail pages
- Sitemaps: combined homepage + Wagtail sitemaps at `/sitemap.xml`
- `robots.txt` and `ads.txt` served as dynamic templates via `core/urls.py`

### URL Layout

- `/` — landing page (country-aware)
- `/blog/` — Wagtail blog index
- `/admin/` — Django admin
- `/admin_blog/` — Wagtail CMS
- `/chat/api/send/` — WhatsApp proxy endpoint
- `/sitemap.xml`, `/robots.txt`, `/ads.txt`

### Context Processors (auto-injected to all templates)

| Variable | Source | Content |
|----------|--------|---------|
| `{{ site_settings }}` | `config.context_processors.site_settings` | Current CountrySettings |
| `{{ project_analytics }}` | `tracking.context_processors.project_analytics` | TrackingSettings singleton |
| `{{ posts }}` / `{{ 3posts }}` | `blog.context_processors.blog_page` | All / latest 3 blog posts |
| `{{ seo_site_name }}` | `home.context_processors.seo_site_name` | Site name for page titles |

### Deployment

Docker: Python 3.10 Alpine, `entrypoint.sh` runs collectstatic → migrate → gunicorn (3 workers, Unix socket). `deploy.sh` generates nginx + systemd configs. Port mapping: 8887→8000.

## Styling

**Always use Tailwind CSS v4 + DaisyUI v5** for all styling. Never write custom CSS unless strictly necessary.

- Tailwind v4: utility classes, configured via `theme/static_src/styles.css` (not `tailwind.config.js`)
- DaisyUI v5: component classes (`btn`, `card`, `modal`, `badge`, etc.) and theme tokens (`bg-base-100`, `text-primary`, etc.)
- After any CSS change: run `python manage.py tailwind build` (or `tailwind start` for watch mode)
- Output: `static/css/main.css` (built from `theme/static_src/styles.css`)
- Themes are set via `data-theme` on `<html>` — current theme comes from `{{ site_settings.theme }}`
