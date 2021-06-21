from django.db import models
from django.core.validators import MaxValueValidator
from main.models import Employee, Evaluator
from django.urls import reverse


class Task(models.Model):
    PENDING = "pending"
    INPROGRESS = "in progress"
    COMPLETE = "complete"
    STATUS_CHOICES = [
        (PENDING, PENDING),
        (INPROGRESS, INPROGRESS),
        (COMPLETE, COMPLETE)
    ]
    name = models.CharField(max_length=150, blank=False)
    description = models.CharField(max_length=500, blank=False)
    assigned_to = models.ForeignKey(Employee, verbose_name="assigned to", on_delete=models.CASCADE, blank=False)
    evaluator = models.ForeignKey(Evaluator, on_delete=models.CASCADE, blank=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING, blank=True)
    due_date = models.DateField("Date Due", blank=False)
    created = models.DateField(auto_now_add=True)

    def get_edit_url(self):
        return reverse("task_edit", kwargs={
            "id": self.id
        })

    def get_delete_url(self):
        return reverse("task_delete", kwargs={
            "id": self.id
        })

    def __str__(self):
        return self.name.capitalize()


class Progress(models.Model):
    description = models.TextField(blank=False)
    task = models.ForeignKey(Task, blank=False, related_name="progresses", on_delete=models.CASCADE)
    date_added = models.DateField("date added", auto_now_add=True)

    def __str__(self):
        return self.description


class Ratings(models.Model):
    efficiency = models.PositiveIntegerField(blank=False, validators=[MaxValueValidator(5)])
    timeliness = models.PositiveIntegerField(blank=False, validators=[MaxValueValidator(5)])
    quality = models.PositiveIntegerField(blank=False, validators=[MaxValueValidator(5)])
    accuracy = models.PositiveIntegerField(blank=False, validators=[MaxValueValidator(5)])
    performance_average = models.PositiveIntegerField(blank=False, validators=[MaxValueValidator(100)])

    def __str__(self):
        return f"Efficiency: {self.efficiency}"\
               f"Timeliness: {self.timeliness}"\
               f"Quality: {self.quality}"\
               f"Accuracy: {self.accuracy}"\
               f"performance_average: {self.performance_average}"


class Evaluation(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE, blank=False)
    date_evaluated = models.DateField(verbose_name="date evaluated", auto_now_add=True)
    remarks = models.TextField(max_length=300, blank=False)
    ratings = models.OneToOneField(Ratings, on_delete=models.CASCADE)