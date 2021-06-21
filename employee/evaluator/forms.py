from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django import forms
from .models import Task, Progress


class AuthenticationForm(forms.Form):
    
    email = forms.EmailField()
    password = forms.CharField(
        widget = forms.PasswordInput()
    )

    def clean_email(self):
        return self.cleaned_data['email'].lower()


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = "__all__"


class ProgressForm(forms.ModelForm):
    
    complete = forms.BooleanField(required=False)

    class Meta:
        model = Progress
        fields = ["description", "complete"]