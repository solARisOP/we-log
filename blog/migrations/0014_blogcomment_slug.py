# Generated by Django 4.2.5 on 2023-10-09 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_alter_post_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogcomment',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]
