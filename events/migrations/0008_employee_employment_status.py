# Generated by Django 4.2.5 on 2023-10-05 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_department_group_specialization_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='employment_status',
            field=models.BooleanField(default=True),
        ),
    ]
