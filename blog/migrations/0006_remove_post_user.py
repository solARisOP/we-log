# Generated by Django 4.2.5 on 2023-09-28 11:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_post_user_alter_post_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='user',
        ),
    ]