# Generated by Django 5.0.2 on 2025-06-21 06:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_like_time_update'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='time_update',
        ),
    ]
