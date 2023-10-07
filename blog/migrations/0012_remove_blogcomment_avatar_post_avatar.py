# Generated by Django 4.2.5 on 2023-10-07 13:32

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_alter_blogcomment_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogcomment',
            name='avatar',
        ),
        migrations.AddField(
            model_name='post',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=blog.models.post_directory_path),
        ),
    ]
