from django import forms
from .models import (
    Designation, Department,
    Evaluator, Employee
)
from django.conf import settings


class DepartmentForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = "__all__"

    def clean_name(self):
        return self.cleaned_data['name'].lower()

    def clean_description(self):
        return self.cleaned_data['description'].lower()

class DesignationForm(forms.ModelForm):

    class Meta:
        model = Designation
        fields = "__all__"

    def clean_name(self):
        return self.cleaned_data['name'].lower()
    
    def clean_description(self):
        return self.cleaned_data['description'].lower()


class EvaluatorForm(forms.ModelForm):

    class Meta:
        model = Evaluator
        fields = "__all__"

class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = "__all__"

    def clean_github(self):
        return self.cleaned_data["github"].lower()