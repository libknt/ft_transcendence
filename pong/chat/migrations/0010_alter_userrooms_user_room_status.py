# Generated by Django 5.0.3 on 2024-09-29 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0009_userblock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrooms',
            name='user_room_status',
            field=models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('invited', 'Invited'), ('ready', 'Ready')], default='active', max_length=8),
        ),
    ]
