from django.conf import settings


def google_site_verification(request):
    return {"GOOGLE_SITE_VERIFICATION": settings.GOOGLE_SITE_VERIFICATION}
