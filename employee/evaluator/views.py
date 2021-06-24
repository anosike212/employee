from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login as DjLogin, logout as DjLogout
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import AuthenticationForm
from main.models import *
from evaluator.models import *
from main.forms import (
    DepartmentForm, DesignationForm,
    EvaluatorForm, EmployeeForm)
from evaluator.forms import (
    TaskForm, ProgressForm, EvaluationForm, RatingsForm)
from .models import *
from .utils import perf_averager
from user.forms import UserCreationForm
from datetime import date
from urllib.parse import urlparse
import json
# Create your views here.

User = get_user_model()

COLORS = ["bg-red", "bg-teal", "bg-blue", "bg-amber"]

def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        form_data = {
            'email': email,
            'password': password
        }
        form = AuthenticationForm(form_data)
        print(form)
        if form.is_valid():
            user = authenticate(email=email, password=password)
            if user:
                DjLogin(request, user)
                return redirect("home")
            else:
                # form.non_field_errors.append("Email/Password is Invalid")
                return render(request, "evaluator/login.html", {"form": form, "errors": ["Email/Password is invalid"]})
        else:
            return render(request, "evaluator/login.html", {"form": form})
    return render(request, "evaluator/login.html")

def logout(request):
    DjLogout(request)
    return redirect("login")

def test(request):
    return HttpResponse(f"{request.user.email}")

def home(request):
    departments = Department.objects.count()
    designations = Designation.objects.count()
    users = get_user_model().objects.count()
    employees = Employee.objects.count()
    evaluators = Evaluator.objects.count()
    tasks = Task.objects.count()
    context = {
        "departments": departments,
        "designations": designations,
        "users": users,
        "employees": employees,
        "evaluators": evaluators,
        "tasks": tasks
    }
    print(context)
    return render(request, "evaluator/home.html", context)

def department_list(request):
    departments = Department.objects.all()
    return render(request, "evaluator/department_list.html", {"departments": departments})

def designation_list(request):
    designations = Designation.objects.all()
    return render(request, "evaluator/designation_list.html", {"designations": designations})

def department_new(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            print(request.POST["name"], request.POST["description"])
            form.save()
            messages.add_message(request, messages.SUCCESS, "Department created successfully")
            return redirect("department_list")
        else:
            return render(request, "evaluator/department_new.html", {"form": form})
    return render(request, "evaluator/department_new.html")

def designation_new(request):
    if request.method == "POST":
        form = DesignationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Designation created successfully")
            return redirect("designation_list")
        else:
            return render(request, "evaluator/designation_new.html", {"form": form})
    return render(request, "evaluator/designation_new.html")

def department_edit(request, id):
    department = get_object_or_404(Department, id=id)
    context = {"department": department}
    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, f"{department.name.title()} Department updated successfully!")
            return redirect("department_list")
        else:
            context.update({"form": form})
            return render(request, "evaluator/department_edit.html", context)
    department = get_object_or_404(Department, id=id)
    form = DepartmentForm(instance=department)
    context.update({"form": form})
    return render(request, "evaluator/department_edit.html", context)

def designation_edit(request, id):
    designation = get_object_or_404(Designation, id=id)
    context = {"designation": designation}
    if request.method == "POST":
        form = DesignationForm(request.POST, instance=designation)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, f"{designation.name.title()} Designation updated successfully!")
            return redirect("designation_list")
        else:
            context.update({"form": form})
            return render(request, "evaluator/designation_edit.html", context)
    form = DesignationForm(instance=designation)
    context.update({"form": form})
    return render(request, "evaluator/designation_edit.html", context)

def department_delete(request, id):
    department = get_object_or_404(Department, id=id)
    department.delete()
    messages.add_message(request, messages.SUCCESS, f"{department.name.title() } Department deleted successfully!")
    return redirect("department_list")

def designation_delete(request, id):
    designation = get_object_or_404(Designation, id=id)
    designation.delete()
    messages.add_message(request, messages.SUCCESS, f"{designation.name.title()} Designation deleted successfully!")
    return redirect("designation_list")

def evaluator_list(request):
    evaluators = Evaluator.objects.all()
    return render(request, "evaluator/evaluator_list.html", {"evaluators": evaluators})

def evaluator_new(request):
    if request.POST:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            avatar = request.FILES.get("avatar")
            evaluator = Evaluator.objects.create(
                avatar=avatar,
                user = user
            )
            messages.add_message(request, messages.SUCCESS, f"Evaluator with email: {user.email} created successfully")
            return redirect("evaluator_list")
        else:
            return render(request, "evaluator/evaluator_new.html", {"form": form})
    return render(request, "evaluator/evaluator_new.html")

def evaluator_detail(request, id):
    evaluator = get_object_or_404(Evaluator, id=id)
    return render(request, "evaluator/evaluator_detail.html", {"evaluator": evaluator})

def evaluator_edit(request, id):
    evaluator = get_object_or_404(Evaluator, id=id)
    context = {"evaluator": evaluator}
    if request.method == "POST":
        my_dict = {key: request.POST[key] for key in request.POST.keys()}
        user = User.objects.get(email=request.POST["hidden_email"])
        my_dict.update({"password1": user.password, "password2": user.password})
        user_form = UserCreationForm(my_dict, instance=user)
        if user_form.is_valid():
            user = user_form.save()
            avatar = request.FILES.get("avatar")
            if avatar:
                evaluator.avatar = avatar
                evaluator.user = user
                evaluator.save()
            messages.add_message(request, messages.SUCCESS, f"user with email: {user.email} updated successfully")
            return redirect("evaluator_list")
        else:
            context.update({"form": user_form})
            return render(request, "evaluator/evaluator_edit.html", context)
    form = UserCreationForm(instance=evaluator.user)
    context.update({"form": form})
    return render(request, "evaluator/evaluator_edit.html", context)

def evaluator_delete(request, id):
    evaluator = Evaluator.objects.get(id=id)
    evaluator.user.delete()
    messages.add_message(request, messages.SUCCESS, f"user with email: {evaluator.user.email} delete successfully")
    return redirect("evaluator_list")

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, "evaluator/employee_list.html", {"employees": employees})

def employee_new(request):
    designations = Designation.objects.all()
    departments = Department.objects.all()
    context = {"designations": designations, "departments": departments}
    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        employee_form = EmployeeForm(request.POST, request.FILES)
        if user_form.is_valid() and employee_form.is_valid():
            user = user_form.save()
            employee = employee_form.save(commit=False)
            employee.user = user
            employee.save()
            employee.designations.set(employee_form.cleaned_data["designations"])
            employee.departments.set(employee_form.cleaned_data["departments"])
            messages.add_message(request, messages.SUCCESS, f"Employee with email: {user.email} created successfully")
            return redirect("employee_list")
        context.update({"employee_form": employee_form, "user_form": user_form})
        return render(request, "evaluator/employee_new.html", context)
    return render(request, "evaluator/employee_new.html", context)

def employee_update(request, id):
    employee = get_object_or_404(Employee, id=id)
    context = {"employee": employee, "colors": COLORS}
    return render(request, "evaluator/employee_detail.html", context)

def employee_edit(request, id):
    employee = get_object_or_404(Employee, id=id)
    designations = Designation.objects.all()
    departments = Department.objects.all()
    context = {"employee": employee, "designations": designations, "departments": departments}
    if request.method == "POST":
        user = employee.user
        my_dict = {key: request.POST[key] for key in request.POST.keys()}
        my_dict.update({"password1": user.password, "password2": user.password})
        form = UserCreationForm(my_dict, instance=user)
        employee_form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid() and employee_form.is_valid():
            user = form.save()
            employee = employee_form.save(commit=False)
            employee.user = user
            employee.save()
            employee.departments.set(employee_form.cleaned_data["departments"])
            employee.designations.set(employee_form.cleaned_data["designations"])
            messages.add_message(request, messages.SUCCESS, f"Employee with email: {user.email} updated successfully")
            return redirect("employee_list")
        else:
            print(form, "\n************", employee_form)
        context.update({"form": form, "employee_form": employee_form})
        return render(request, "evaluator/employee_edit.html", context)
    form = UserCreationForm(instance=employee.user)
    employee_form = EmployeeForm(instance=employee)
    print(employee_form)
    context.update({"form": form, "employee_form": employee_form})
    return render(request, "evaluator/employee_edit.html", context)

def employee_delete(request, id):
    employee = get_object_or_404(Employee, id=id)
    employee.user.delete()
    messages.add_message(request, messages.SUCCESS, f"Employee with email: {employee.user.email} deleted successfully")
    return redirect("employee_list")

def task_list(request):
    tasks = Task.objects.all()
    COLORS = {
        "pending": "bg-cyan",
        "in progress": "bg-orange",
        "complete": "bg-red",
    }
    return render(request, "evaluator/task_list.html", {"tasks": tasks, "date": date.today()})

def task_new(request):
    print(f"request path: {request.path}\nrequest full path: {request.get_full_path()}\nuser: {request.user}")
    print(urlparse(request.get_full_path()).query.split("="))
    evaluators = Evaluator.objects.all()
    employees = Employee.objects.all()
    context = {"evaluators": evaluators, "employees": employees}
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            messages.add_message(request, messages.SUCCESS, f"\"{task.name.title()}\" task created successfully")
            return redirect("task_list")
        context.update({"form": form})
        return render(request, "evaluator/task_new.html", context)
    return render(request, "evaluator/task_new.html", context)

def task_edit(request, id):
    task = get_object_or_404(Task, id=id)
    evaluators = Evaluator.objects.all()
    employees = Employee.objects.all()
    context = {"evaluators": evaluators, "employees": employees, "task": task}
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, f"\"{task.name.title()}\" task updated successfully")
            return redirect("task_list")
        context.update({'form': form})
        return render(request, "evaluator/task_edit.html", context)
    form = TaskForm(instance=task)
    context.update({"form": form})
    return render(request, "evaluator/task_edit.html", context)

def task_delete(request, id):
    task = get_object_or_404(Task, id=id)
    task.delete()
    messages.add_message(request, messages.SUCCESS, f"\"{task.name.title()}\" task deleted successfully")
    return redirect("task_list")

def progress_new(request, id):
    task = get_object_or_404(Task, id=id)
    if task.status == "complete":
        return HttpResponse("Cannot add anymore progress to this task")
    if request.method == "POST":
        form = ProgressForm(request.POST)
        if form.is_valid():
            progress = form.save(commit=False)
            if request.POST.get("complete"):
                task.status = "complete"
                task.save()
            else:
                task.status = "in progress"
                task.save()
            progress.task = task
            progress.save()
            messages.add_message(request, messages.SUCCESS, "Progress added successfully")
            return redirect("task_list")
        return render(request, "evaluator/progress_new.html")

    form = ProgressForm()
    return render(request, "evaluator/progress_new.html")

def progress_detail(request, id):
    task = get_object_or_404(Task, id=id)
    progresses = task.progresses.all()
    progresses_dict = [
        {"description": progress.description}
        for progress in progresses
    ]
    complete_res = {
        "complete": True if task.status == "complete" else False,
        "progresses": progresses_dict
    }
    return HttpResponse(
        json.dumps(complete_res),
        content_type="application/json"
    )

def evaluation_list(request):
    evaluations = Evaluation.objects.all()
    return render(request, "evaluator/evaluation_list.html", {"evaluations": evaluations})

def evaluation_new(request, id):
    task = get_object_or_404(Task, id=id)
    if task.status != "complete":
        error_msg = "You can only evaluate this task once it has been completed!"
        url = reverse("evaluation_list")
        context = {"error_msg": error_msg, "url": url}
        return render(request, "evaluator/error.html", context)
    context = {"task": task, "count": range(1, 6)}
    if request.method == "POST":
        rating_form = RatingsForm(request.POST)
        form = EvaluationForm(request.POST)
        if rating_form.is_valid() and form.is_valid():
            ratings = rating_form.save(commit=False)
            perf_avg = perf_averager(rating_form)
            ratings.performance_average = perf_avg
            ratings.save()
            evaluation = form.save(commit=False)
            evaluation.task = task
            evaluation.ratings = ratings
            evaluation.save()
            messages.add_message(request, messages.SUCCESS, "Evaluation edited successfully")
            return redirect("evaluation_list")
        context.update({"form": form, "rating_form": rating_form})
        return render(request, "evaluator/evaluation_new.html", context)
    return render(request, "evaluator/evaluation_new.html", context)

def evaluation_edit(request, id):
    task = get_object_or_404(Task, id=id)
    evaluation = task.evaluation
    ratings = evaluation.ratings
    context = {"evaluation": evaluation, "count": range(1, 6)}
    if request.method == "POST":
        rating_form = RatingsForm(request.POST, instance=ratings)
        form = EvaluationForm(request.POST, instance=evaluation)
        if rating_form.is_valid() and form.is_valid():
            ratings = rating_form.save(commit=False)
            perf_avg = perf_averager(rating_form)
            ratings.performance_average = perf_avg
            ratings.save()
            evaluation = form.save(commit=False)
            evaluation.task = task
            evaluation.ratings = ratings
            evaluation.save()
            messages.add_message(request, messages.SUCCESS, "Evaluation edited successfully")
            return redirect("evaluation_list")
        context.update({"form": form, "rating_form": rating_form})
        return render(request, "evaluator/evaluation_edit.html", context)
    form = EvaluationForm(instance=evaluation)
    rating_form = RatingsForm(instance=ratings)
    print(rating_form)
    context.update({"form": form, "rating_form": rating_form})
    return render(request, "evaluator/evaluation_edit.html", context)