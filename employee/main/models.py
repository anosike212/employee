from django.db import models
from django.conf import settings
from django.urls import reverse


class Designation(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)

    def get_edit_url(self):
        return reverse("designation_edit", kwargs={
            "id": self.id
        })

    def get_delete_url(self):
        return reverse("designation_delete", kwargs={
            "id": self.id
        })

    def __str__(self):
        return self.name.title()


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)

    def get_edit_url(self):
        return reverse("department_edit", kwargs={
            "id": self.id
        })

    def get_delete_url(self):
        return reverse("department_delete", kwargs={
            "id": self.id
        })

    def __str__(self):
        return self.name.title()


class Option(models.Model):
    a = models.CharField(max_length=300, blank=False)
    b = models.CharField(max_length=300, blank=False)
    c = models.CharField(max_length=300, blank=False)
    d = models.CharField(max_length=300, blank=False)

    def __Str__(self):
        return [
            ("a", self.a),
            ("b", self.b),
            ("c", self.c),
            ("d", self.d),
        ]


class Question(models.Model):
    description = models.TextField(blank=False)
    options = models.OneToOneField(Option, blank=False, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1, blank=False)

    def __str__(self):
        return self.description


class TestResult(models.Model):
    correct = models.PositiveIntegerField(default=0)
    incorrect = models.PositiveIntegerField(default=0)
    score = models.PositiveIntegerField(default=0)


class RegularUser(models.Model):
    avatar = models.ImageField(upload_to="reg_users/")
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name} {self.user.middle_name}"


class Evaluator(models.Model):
    avatar = models.ImageField(upload_to="evaluators/")
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 

    def get_absolute_url(self):
        return reverse("evaluator_detail", kwargs={
            "id": self.id
        })

    def get_edit_url(self):
        return reverse("evaluator_edit", kwargs={
            "id": self.id
        })

    def get_delete_url(self):
        return reverse("evaluator_delete", kwargs={
            "id": self.id
        })

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name} {self.user.middle_name}"


class Employee(models.Model):
    avatar = models.ImageField(upload_to="employee/", blank=True)
    cv = models.FileField(upload_to="cvs", blank=True)
    github = models.URLField(verbose_name="github page", max_length=200, blank=True)
    designations = models.ManyToManyField(Designation, related_name="employees", blank=False)
    departments = models.ManyToManyField(Department, related_name="employees", blank=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
    created = models.DateField(verbose_name="date created", auto_now_add=True)

    def get_absolute_url(self):
        return reverse("employee_update", kwargs={
            "id": self.id
        })

    def get_edit_url(self):
        return reverse("employee_edit", kwargs={
            "id": self.id
        })

    def get_delete_url(self):
        return reverse("employee_delete", kwargs={
            "id": self.id
        })

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name} {self.user.middle_name}"


class Applicant(models.Model):
    avatar = models.ImageField(upload_to="employee/", blank=False)
    cv = models.FileField(upload_to="cvs", blank=False)
    github = models.URLField(verbose_name="github page", max_length=200, blank=False)
    designation = models.ManyToManyField(Designation, related_name="applicants", blank=False)
    department = models.ManyToManyField(Department, related_name="applicants", blank=False)
    status = models.CharField(max_length=30, default="pending")
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test = models.ManyToManyField(Question, through="QuestionAnswered")
    test_result = models.OneToOneField(TestResult, verbose_name="test result", blank=True, on_delete=models.CASCADE)
    created = models.DateField(verbose_name="date created", auto_now_add=True)

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name} {self.user.middle_name}"


class QuestionAnswered(models.Model):
    user = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1, blank=True)

    class Meta:
        verbose_name = "Question Answered"
        verbose_name_plural = "Questions Answered"