from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^applicant/", views.signup, name="signup"),
]