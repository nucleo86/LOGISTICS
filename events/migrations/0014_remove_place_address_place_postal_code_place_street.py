# Generated by Django 4.2.5 on 2023-10-06 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_place_city'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='place',
            name='address',
        ),
        migrations.AddField(
            model_name='place',
            name='postal_code',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='place',
            name='street',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
    ]
