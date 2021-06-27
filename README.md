# employee
cs project

# install django
# run >>python manage.py runserver in the employee folder

********USE GIT PULL**********

# run >> python manage.py shell
>>from django.contrib.auth import get_user_model\n
>>User = get_user_model()\n
>>User.objects.create_superuser(username="*****", email="******", password="******")\n

go to localhost:8000/admin/home in your browser
input your login details as a superuser
