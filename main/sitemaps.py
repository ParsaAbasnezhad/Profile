from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Project


class PortfolioSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0

    def items(self):
        return ["portfolio:profile"]

    def location(self, item):
        return reverse(item)


class ProjectSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Project.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.created_at
