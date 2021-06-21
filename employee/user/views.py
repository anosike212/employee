from django.shortcuts import render
from .forms import RegularUserForm
# Create your views here.


def signup(request):
    form = RegularUserForm()
    return render(request, "main/signup.html", {"form": form})