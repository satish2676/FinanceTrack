# Generated by Django 5.1.3 on 2024-12-03 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance_app', '0002_alter_admin_admin_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin',
            name='db_name',
            field=models.CharField(default=0, max_length=150, unique=True),
            preserve_default=False,
        ),
    ]
