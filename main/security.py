"""Shared security helpers for input sanitization, rate limiting, and SVG filtering."""

from __future__ import annotations

import logging
import re
import xml.etree.ElementTree as ET
from html import escape

from django.conf import settings
from django.core.cache import cache
from django.http import HttpRequest, JsonResponse

logger = logging.getLogger("main.security")

CONTROL_CHARS_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
DANGEROUS_URI_RE = re.search if False else re.compile(
    r"javascript:|data:|vbscript:|expression\s*\(",
    re.IGNORECASE,
)

ALLOWED_SVG_TAGS = {
    "path",
    "rect",
    "circle",
    "ellipse",
    "line",
    "polyline",
    "polygon",
    "g",
}
ALLOWED_SVG_ATTRS = {
    "d",
    "fill",
    "stroke",
    "stroke-width",
    "stroke-linecap",
    "stroke-linejoin",
    "stroke-miterlimit",
    "fill-rule",
    "clip-rule",
    "cx",
    "cy",
    "r",
    "rx",
    "ry",
    "x",
    "y",
    "x1",
    "y1",
    "x2",
    "y2",
    "width",
    "height",
    "transform",
    "points",
    "opacity",
    "fill-opacity",
    "stroke-opacity",
    "viewbox",
}

MAX_JSON_BODY_BYTES = 8 * 1024


def get_client_ip(request: HttpRequest) -> str:
    if getattr(settings, "TRUST_X_FORWARDED_FOR", False):
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
        if forwarded:
            return forwarded.split(",", 1)[0].strip()[:45]
    return (request.META.get("REMOTE_ADDR") or "0.0.0.0")[:45]


def get_user_agent(request: HttpRequest) -> str:
    return (request.META.get("HTTP_USER_AGENT") or "")[:256]


def sanitize_text(value: str, *, keep_newlines: bool = False) -> str:
    text = CONTROL_CHARS_RE.sub("", value or "")
    if keep_newlines:
        return text.replace("\r\n", "\n").replace("\r", "\n").strip()
    return " ".join(text.split())


def _serialize_svg_element(el: ET.Element) -> str:
    tag = el.tag.split("}", 1)[-1].lower()
    if tag not in ALLOWED_SVG_TAGS:
        return ""

    attrs: list[str] = []
    for raw_name, raw_value in el.attrib.items():
        name = raw_name.split("}", 1)[-1].lower()
        if name.startswith("on") or name not in ALLOWED_SVG_ATTRS:
            continue
        value = (raw_value or "").strip()
        if not value or DANGEROUS_URI_RE.search(value):
            continue
        attrs.append(f'{name}="{escape(value, quote=True)}"')

    inner = "".join(_serialize_svg_element(child) for child in list(el))
    attr_str = f" {' '.join(attrs)}" if attrs else ""
    if inner:
        return f"<{tag}{attr_str}>{inner}</{tag}>"
    return f"<{tag}{attr_str}/>"


def sanitize_svg_fragment(raw: str | None) -> str:
    text = (raw or "").strip()
    if not text:
        return ""
    wrapped = f"<g>{text}</g>"
    try:
        root = ET.fromstring(wrapped)
    except ET.ParseError:
        try:
            root = ET.fromstring(wrapped.replace("&", "&amp;"))
        except ET.ParseError:
            return ""
    return "".join(_serialize_svg_element(child) for child in list(root))


def rate_limit_exceeded(request: HttpRequest, scope: str, limit: int, window_seconds: int) -> bool:
    ip = get_client_ip(request)
    key = f"rl:{scope}:{ip}"
    if cache.add(key, 1, window_seconds):
        return False
    try:
        count = cache.incr(key)
    except ValueError:
        cache.set(key, 1, window_seconds)
        return False
    if count > limit:
        logger.warning("Rate limit exceeded scope=%s ip=%s count=%s", scope, ip, count)
        return True
    return False


def too_many_requests_response() -> JsonResponse:
    return JsonResponse(
        {"ok": False, "error": "Too many requests. Please try again later."},
        status=429,
    )
