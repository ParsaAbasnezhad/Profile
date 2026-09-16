"""
URL configuration for parsaabasnezhad project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.urls import include, path
from main.sitemaps import PortfolioSitemap, ProjectSitemap

handler404 = "main.views.error_404_view"
handler500 = "main.views.error_500_view"

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": {"portfolio": PortfolioSitemap, "projects": ProjectSitemap}},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path('', include('main.urls')),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
