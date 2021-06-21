from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^login/$", views.login, name="login"),
    url(r"^logout/$", views.logout, name="logout"),
    url(r"^test/$", views.test, name="test"),
    url(r"^home/$", views.home, name="home"),
    url(r"^department/list/", views.department_list, name="department_list"),
    url(r"^department/new", views.department_new, name="department_new"),
    url(r"^department/(?P<id>\d+)/edit/$", views.department_edit, name="department_edit"),
    url(r"^department/(?P<id>\d+)/delete/$", views.department_delete, name="department_delete"),
    url(r"^designation/list/", views.designation_list, name="designation_list"),
    url(r"^designation/new", views.designation_new, name="designation_new"),
    url(r"^designation/(?P<id>\d+)/edit/$", views.designation_edit, name="designation_edit"),
    url(r"^designation/(?P<id>\d+)/delete/$", views.designation_delete, name="designation_delete"),
    url(r"^evaluator/list/", views.evaluator_list, name="evaluator_list"),
    url(r"^evaluator/new", views.evaluator_new, name="evaluator_new"),
    url(r"^evaluator/(?P<id>\d+)/detail/$", views.evaluator_detail, name="evaluator_detail"),
    url(r"^evaluator/(?P<id>\d+)/edit/$", views.evaluator_edit, name="evaluator_edit"),
    url(r"^evaluator/(?P<id>\d+)/delete/$", views.evaluator_delete, name="evaluator_delete"),
    url(r"^employee/list/", views.employee_list, name="employee_list"),
    url(r"^employee/new", views.employee_new, name="employee_new"),
    url(r"^employee/(?P<id>\d+)/detail/$", views.employee_update, name="employee_update"),
    url(r"^employee/(?P<id>\d+)/edit/$", views.employee_edit, name="employee_edit"),
    url(r"^employee/(?P<id>\d+)/delete/$", views.employee_delete, name="employee_delete"),
    url(r"^task/list/$", views.task_list, name="task_list"),
    url(r"^task/new$", views.task_new, name="task_new"),
    url(r"^task/(?P<id>\d+)/edit/$", views.task_edit, name="task_edit"),
    url(r"^task/(?P<id>\d+)/delete/$", views.task_delete, name="task_delete"),
    url(r"^task/(?P<id>\d+)/progress/new$", views.progress_new, name="progress")
]