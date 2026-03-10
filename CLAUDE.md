# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Django + Wagtail CMS project for a septic tank cleaning service (limpiezapozossepticos.com). Multi-country landing page system with blog, SEO, analytics, and WhatsApp chat integration.

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
| `blog` | Wagtail blog (BlogPage, BlogIndexPage), BaseStreamBlock, templatetags, wagtail icons |
| `config` | CountrySettings, metadata mixins (MetadataPageMixin), CountryMiddleware |
| `analytics` | AnalyticsSettings singleton (GA4/GTM IDs) |
| `tracking` | TrackingSettings — raw HTML/JS snippets injected into templates |
| `chat` | WhatsApp API endpoint at `/chat/api/send/` |
| `theme` | Tailwind CSS + DaisyUI config |
| `favicon` | Favicon management |

### Multi-Country Landing Pages

`LandingPage` (in `home/`) is a plain Django model (not Wagtail). Fallback chain: requested country → Bolivia default → first enabled → first available. Each country is a `CountrySettings` instance; middleware auto-detects and attaches to `request.country`.

### SEO System

- `config.metadata.MetadataPageMixin` provides search_image and promote_panels for Wagtail pages (seo_title, search_description are built-in)
- Sitemaps: combined homepage + Wagtail sitemaps at `/sitemap.xml`
- `robots.txt` and `ads.txt` served as dynamic templates via `core/urls.py`

### Analytics & Tracking

Two separate models:
- `AnalyticsSettings` — project-level IDs (GA4, GTM, Google Ads conversion IDs)
- `TrackingSettings` — raw HTML/JS snippets (GTM, GA, Ads, AdSense, Meta Pixel, Open Graph, custom head/body scripts)

Both are injected into all templates via context processors.

### URL Layout

- `/` — landing page (country-aware)
- `/blog/` — Wagtail blog index
- `/admin/` — Django admin
- `/admin_blog/` — Wagtail CMS
- `/chat/api/send/` — WhatsApp chat API
- `/sitemap.xml`, `/robots.txt`, `/ads.txt`

### Context Processors (auto-injected to all templates)

- `wagtail.contrib.settings.context_processors.settings`
- `blog.context_processors.blog_page`
- `config.context_processors.site_settings`
- `analytics.context_processors.project_analytics`
- `home.context_processors.seo_site_name`

### Deployment

Docker: Python 3.10 Alpine, `entrypoint.sh` runs collectstatic → migrate → gunicorn (3 workers, Unix socket). `deploy.sh` generates nginx + systemd configs. Port mapping: 8887→8000.
