from django.urls import path

from . import views

app_name = "portfolio"

urlpatterns = [
    path("", views.profile_view, name="profile"),
    path("projects/<slug:slug>/", views.project_detail_view, name="project_detail"),
    path("visit/", views.visit_page_view, name="visit"),
    path("robots.txt", views.robots_txt, name="robots"),
    path("contact/", views.contact_message_create, name="contact_message_create"),
    path("visit-request/", views.visit_request_create, name="visit_request_create"),
]
