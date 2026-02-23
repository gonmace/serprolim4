"""Custom sitemaps for pages not managed by Wagtail."""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone


class HomepageSitemap(Sitemap):
    """Sitemap for the homepage (landing) served by Django view."""
    changefreq = "weekly"
    priority = 1.0

    def items(self):
        return [True]  # Single item to generate one URL

    def location(self, item):
        return "/"

    def lastmod(self, item):
        return timezone.now()
