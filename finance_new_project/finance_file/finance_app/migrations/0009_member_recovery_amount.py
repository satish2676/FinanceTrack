# Generated by Django 5.1.3 on 2024-12-14 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance_app', '0008_alter_member_end_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='recovery_amount',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=10),
        ),
    ]
