"""Extra security headers and admin-login brute-force protection."""

from __future__ import annotations

from django.conf import settings
from django.http import HttpRequest, HttpResponse

from .security import rate_limit_exceeded

PERMISSIONS_POLICY = (
    "accelerometer=(), autoplay=(), camera=(), display-capture=(), geolocation=(), "
    "gyroscope=(), magnetometer=(), microphone=(), payment=(), publickey-credentials-get=(), "
    "usb=()"
)


class ExtraSecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.admin_prefix = "/" + settings.ADMIN_URL.lstrip("/")
        self.media_prefix = settings.MEDIA_URL

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)
        response.headers.setdefault("Permissions-Policy", PERMISSIONS_POLICY)
        response.headers.setdefault("X-Permitted-Cross-Domain-Policies", "none")
        response.headers.setdefault("Cross-Origin-Resource-Policy", "same-origin")
        response.headers.setdefault("X-DNS-Prefetch-Control", "off")
        response.headers.setdefault("X-Content-Type-Options", "nosniff")

        path = request.path
        if path.startswith(self.admin_prefix):
            response["Cache-Control"] = "no-store"
            response["Pragma"] = "no-cache"

        if path.startswith(self.media_prefix) and path.lower().endswith(".svg"):
            response["Content-Security-Policy"] = (
                "default-src 'none'; style-src 'unsafe-inline'; sandbox"
            )
            response["X-Content-Type-Options"] = "nosniff"

        return response


class AdminLoginRateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.login_path = "/" + settings.ADMIN_URL.lstrip("/") + "login/"
        self.limit, self.window = settings.ADMIN_LOGIN_RATE_LIMIT

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if request.method == "POST" and request.path.rstrip("/") + "/" == self.login_path:
            if rate_limit_exceeded(request, "admin-login", self.limit, self.window):
                return HttpResponse(
                    "Too many login attempts. Please try again later.",
                    status=429,
                    content_type="text/plain; charset=utf-8",
                )
        return self.get_response(request)
