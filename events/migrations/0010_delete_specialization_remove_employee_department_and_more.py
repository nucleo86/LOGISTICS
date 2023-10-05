# Generated by Django 4.2.5 on 2023-10-05 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_delete_employeespecialization'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Specialization',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='department',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='employment_status',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='groups',
        ),
        migrations.DeleteModel(
            name='Department',
        ),
        migrations.DeleteModel(
            name='Group',
        ),
    ]
