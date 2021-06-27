# This should be done in the shell i.e python manage.py shell
  `>> from django.contrib.auth.models import Group, Permission`  
  `>> emp = Group.objects.create(name="employees")`  
  `>> eva = Group.objects.create(name="evaluators")`  
      >> eva.permissions.set([
  >>  Permission.objects.get(codename="add_evaluation),
  >>  Permission.objects.get(codename="change_evaluation"),
  >>  Permission.objects.get(codename="view_evaluation"),
  >>  Permission.objects.get(codename="view_progress"),
  >>  Permission.objects.get(codename="view_task")
  >>  ])
  >> emp.permissions.set([
  >>  Permission.objects.get(codename="add_progress"),
  >>  Permission.objects.get(codename="view_progress"),
  >>  Permission.objects.get(codename="view_task"),
  >>  ])
  >> emp.save() # just in case
  >> eva.save() # just in case
