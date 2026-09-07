from django.urls import path

from . import views


app_name = "main"

urlpatterns = [
    path("", views.home, name="home"),
    path("projects/protectx/", views.protectx, name="protectx"),
    path("projects/kahoot/", views.kahoot, name="kahoot"),
]