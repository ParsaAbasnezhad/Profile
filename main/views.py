import json

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.utils.safestring import mark_safe
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

from .forms import ContactMessageForm, VisitRequestForm
from .models import ContactLink, ContactMessage, Profile, Project, Quote, SkillCategory, VisitRequest
from .security import MAX_JSON_BODY_BYTES, rate_limit_exceeded, too_many_requests_response


def error_404_view(request, exception):
    return render(request, "404.html", status=404)


def error_500_view(request):
    return render(request, "500.html", status=500)


def robots_txt(request):
    sitemap_url = request.build_absolute_uri("/sitemap.xml")
    return HttpResponse(
        "User-agent: *\n"
        f"Disallow: /{settings.ADMIN_URL}\n"
        "Disallow: /contact/\n"
        "Disallow: /visit-request/\n"
        f"Sitemap: {sitemap_url}\n",
        content_type="text/plain",
    )


def csrf_failure(request, reason=""):
    return JsonResponse(
        {"ok": False, "error": "Your session has expired. Please refresh the page and try again."},
        status=403,
    )


def _seo_json_ld(request, profile, project=None):
    person_name = profile.full_name if profile else "Parsa Abasnezhad"
    role_title = profile.role_title if profile else "Python and full-stack developer"
    description = (
        profile.tagline
        if profile and profile.tagline
        else f"{person_name} is a {role_title} specializing in Python, Django and modern web development."
    )
    data = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": person_name,
        "url": request.build_absolute_uri("/"),
        "jobTitle": role_title,
        "description": description,
        "knowsAbout": ["Python", "Django", "Full-stack development", "Web development"],
    }
    if project:
        data = {
            "@context": "https://schema.org",
            "@type": "CreativeWork",
            "name": project.title,
            "url": request.build_absolute_uri(project.get_absolute_url()),
            "description": project.description,
            "author": {
                "@type": "Person",
                "name": person_name,
                "url": request.build_absolute_uri("/"),
            },
        }
    serialized = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
    return mark_safe(serialized)


def profile_view(request):
    """Renders the single-page portfolio (hero, now-building, projects, skills, about, contacts)."""
    profile = Profile.objects.prefetch_related("stats", "now_building").first()
    now_building = None
    if profile:
        now_building = profile.now_building.filter(is_active=True).first()

    context = {
        "profile": profile,
        "now_building": now_building,
        "quote": Quote.objects.filter(is_active=True).order_by("?").first(),
        "projects": Project.objects.filter(is_published=True).prefetch_related("tags"),
        "skill_categories": SkillCategory.objects.prefetch_related("items"),
        "contact_links": ContactLink.objects.all(),
        "seo_json_ld": _seo_json_ld(request, profile),
    }
    return render(request, "portfolio/profile.html", context)


def project_detail_view(request, slug):
    project = get_object_or_404(
        Project.objects.prefetch_related("tags", "features", "gallery_images"),
        slug=slug,
        is_published=True,
    )
    profile = Profile.objects.first()
    next_project = (
        Project.objects.filter(is_published=True, order__gt=project.order)
        .order_by("order")
        .first()
        or Project.objects.filter(is_published=True).exclude(pk=project.pk).order_by("order").first()
    )
    context = {
        "project": project,
        "next_project": next_project,
        "profile": profile,
        "contact_links": ContactLink.objects.all(),
        "seo_json_ld": _seo_json_ld(request, profile, project),
    }
    return render(request, "portfolio/project_detail.html", context)


def visit_page_view(request):
    return render(
        request,
        "portfolio/visit.html",
        {
            "profile": Profile.objects.first(),
            "contact_links": ContactLink.objects.all(),
        },
    )


@require_POST
@csrf_protect
def contact_message_create(request):
    if request.content_type.startswith("application/json"):
        if request.content_length and request.content_length > MAX_JSON_BODY_BYTES:
            return JsonResponse({"ok": False, "error": "Request body is too large."}, status=413)
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return JsonResponse({"ok": False, "error": "Invalid request body."}, status=400)
    else:
        data = request.POST

    if rate_limit_exceeded(request, "contact", *settings.FORM_RATE_LIMIT):
        return too_many_requests_response()
    form = ContactMessageForm(data=data)
    if not form.is_valid():
        return JsonResponse({"ok": False, "errors": form.errors.get_json_data()}, status=400)
    if form.is_honeypot_triggered():
        return JsonResponse({"ok": True, "message": "Your message has been sent. We will contact you soon."})

    ContactMessage.objects.create(
        name=form.cleaned_data["name"],
        contact=form.cleaned_data["contact"],
        message=form.cleaned_data["message"],
    )
    return JsonResponse({"ok": True, "message": "Your message has been sent. We will contact you soon."})


@require_POST
@csrf_protect
def visit_request_create(request):
    if rate_limit_exceeded(request, "visit-request", *settings.FORM_RATE_LIMIT):
        return too_many_requests_response()
    form = VisitRequestForm(data=request.POST)
    if not form.is_valid():
        return JsonResponse({"ok": False, "errors": form.errors.get_json_data()}, status=400)
    if form.is_honeypot_triggered():
        return JsonResponse({"ok": True, "message": "Your visit request has been submitted. We will contact you soon."})
    VisitRequest.objects.create(phone=form.cleaned_data["phone"])
    return JsonResponse({"ok": True, "message": "Your visit request has been submitted. We will contact you soon."})
