# Generated by Django 4.2.5 on 2023-10-06 12:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_department_group_specialization_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='events.specialization'),
        ),
    ]