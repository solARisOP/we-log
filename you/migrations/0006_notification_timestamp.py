# Generated by Django 4.2.5 on 2023-10-10 10:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('you', '0005_rename_read_notification_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='timeStamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
