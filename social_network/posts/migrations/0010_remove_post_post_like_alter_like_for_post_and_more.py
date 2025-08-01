# Generated by Django 5.0.2 on 2025-07-14 16:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_alter_comment_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='post_like',
        ),
        migrations.AlterField(
            model_name='like',
            name='for_post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Пост', to='posts.post'),
        ),
        migrations.AlterField(
            model_name='like',
            name='like_status',
            field=models.CharField(choices=[('like', 'like'), ('none', 'none')], default=None),
        ),
    ]
