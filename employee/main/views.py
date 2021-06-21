from django.shortcuts import render
from django.http import HttpResponse


def landing_page(request):
    return render(request, "main/landingpage.html")

def home_page(request):
    return render(request, "main/index.html")

def login(request):
    return render(request, "main/login.html")

def signup(request):
    return render(request, "main/signup.html")
