# Generated by Django 4.2.5 on 2023-10-09 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('you', '0003_alter_notification_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='read',
            field=models.IntegerField(choices=[(0, 'new'), (1, 'current'), (2, 'read')], default=0),
        ),
    ]