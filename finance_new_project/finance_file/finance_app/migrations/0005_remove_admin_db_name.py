# Generated by Django 5.1.3 on 2024-12-03 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance_app', '0004_alter_admin_admin_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='admin',
            name='db_name',
        ),
    ]
