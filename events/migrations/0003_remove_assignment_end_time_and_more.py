# Generated by Django 4.2.5 on 2023-10-03 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_assignment_end_time_assignment_start_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='assignment',
            name='start_time',
        ),
    ]