# Generated by Django 3.2.2 on 2021-06-18 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicant',
            name='department',
        ),
        migrations.AddField(
            model_name='applicant',
            name='department',
            field=models.ManyToManyField(related_name='applicants', to='main.Department'),
        ),
        migrations.RemoveField(
            model_name='applicant',
            name='designation',
        ),
        migrations.AddField(
            model_name='applicant',
            name='designation',
            field=models.ManyToManyField(related_name='applicants', to='main.Designation'),
        ),
        migrations.RemoveField(
            model_name='employee',
            name='department',
        ),
        migrations.AddField(
            model_name='employee',
            name='department',
            field=models.ManyToManyField(related_name='employees', to='main.Department'),
        ),
        migrations.RemoveField(
            model_name='employee',
            name='designation',
        ),
        migrations.AddField(
            model_name='employee',
            name='designation',
            field=models.ManyToManyField(related_name='employees', to='main.Designation'),
        ),
    ]
