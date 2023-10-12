# Generated by Django 4.2.5 on 2023-10-11 12:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0017_post_viewcount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='viewCount',
        ),
        migrations.CreateModel(
            name='viewCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cookie', models.CharField(blank=True, max_length=100, null=True)),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='viewcount', to='blog.post')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='viewcount', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]