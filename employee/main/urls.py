from django.conf.urls import url 
from . import views

app_name = "main"

urlpatterns = [
    url(r"^$", views.landing_page, name="landing_page"),
    url(r"^login/$", views.login, name="login"),
    url(r"^signup/$", views.signup, name="signup"),
]
