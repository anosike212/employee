from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):

    username = models.CharField(_('username'), max_length=150, unique=False)
    first_name = models.CharField(_('first name'), max_length=150, blank=False)
    middle_name = models.CharField(_('middle name'), max_length=150, blank=False)
    last_name = models.CharField(_('last name'), max_length=150, blank=False)
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(_('phone number'), max_length=11, unique=True, blank=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []