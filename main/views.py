from django.shortcuts import render


def home(request):
    return render(request, "main/index.html")


def protectx(request):
    return render(request, "main/protext.html")


def kahoot(request):
    return render(request, "main/kahoot.html")
