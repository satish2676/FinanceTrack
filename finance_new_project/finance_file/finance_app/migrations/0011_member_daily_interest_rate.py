# Generated by Django 5.1.3 on 2024-12-15 10:32

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance_app', '0010_remove_member_paid_days_remove_member_unpaid_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='daily_interest_rate',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.10'), max_digits=5),
        ),
    ]