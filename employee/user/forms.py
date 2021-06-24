from django import forms
from django.conf import settings 
from main.models import Applicant, Employee, Evaluator, RegularUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm as MyUserCreationForm
from django.core.exceptions import ValidationError
import re
# from .models import User


class UserCreationForm(MyUserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ["first_name", "middle_name", "last_name", "email", "phone_number"]
    
    def clean_phone_number(self):
        regex = re.compile(r"\d{11}")
        phone_number = self.cleaned_data["phone_number"]
        match = regex.match(phone_number)
        if not match:
            raise ValidationError("Enter a valid phone number")
        return phone_number