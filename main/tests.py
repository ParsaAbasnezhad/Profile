from django.core.cache import cache
from django.test import Client, TestCase, override_settings
from django.middleware.csrf import get_token

from .models import ContactMessage, VisitRequest
from .views import error_500_view


@override_settings(ALLOWED_HOSTS=["example.com"])
class GoogleIntegrationTests(TestCase):
    def test_robots_points_to_sitemap(self):
        response = self.client.get("/robots.txt", headers={"Host": "example.com"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sitemap: http://example.com/sitemap.xml")

    def test_sitemap_is_available(self):
        response = self.client.get("/sitemap.xml", headers={"Host": "example.com"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "/")


@override_settings(DEBUG=False, ALLOWED_HOSTS=["testserver"])
class CustomErrorPageTests(TestCase):
    def test_not_found_uses_custom_error_page(self):
        response = self.client.get("/does-not-exist/")

        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "404", status_code=404)
        self.assertContains(response, "This page hasn't been built yet.", status_code=404)

    def test_server_error_uses_custom_error_page(self):
        response = error_500_view(self.client.get("/").wsgi_request)

        self.assertEqual(response.status_code, 500)
        self.assertContains(response, "500", status_code=500)
        self.assertContains(response, "Something broke on this end.", status_code=500)


@override_settings(ALLOWED_HOSTS=["testserver"])
class PublicFormSecurityTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = Client(enforce_csrf_checks=True)

    def csrf_token(self):
        response = self.client.get("/", secure=True)
        return get_token(response.wsgi_request)

    def test_contact_rejects_missing_csrf_without_server_error(self):
        response = self.client.post(
            "/contact/",
            {"name": "Test User", "contact": "test@example.com", "message": "Hello"},
            secure=True,
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()["ok"], False)

    def test_contact_sanitizes_and_stores_valid_input(self):
        token = self.csrf_token()
        response = self.client.post(
            "/contact/",
            {
                "name": "  Test\x01 User  ",
                "contact": "test@example.com",
                "message": "  Hello\r\nthere  ",
            },
            HTTP_X_CSRFTOKEN=token,
            HTTP_REFERER="https://testserver/",
            secure=True,
        )
        self.assertEqual(response.status_code, 200)
        message = ContactMessage.objects.get()
        self.assertEqual(message.name, "Test User")
        self.assertEqual(message.message, "Hello\nthere")

    def test_visit_normalizes_persian_digits(self):
        token = self.csrf_token()
        response = self.client.post(
            "/visit-request/",
            {"phone": "۰۹۱۲۱۲۳۴۵۶۷"},
            HTTP_X_CSRFTOKEN=token,
            HTTP_REFERER="https://testserver/",
            secure=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(VisitRequest.objects.get().phone, "09121234567")
