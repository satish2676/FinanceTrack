# Generated by Django 5.1.3 on 2024-12-30 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance_app', '0015_remove_member_balance_amount_remove_member_paid_days_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='end_date',
        ),
        migrations.AlterField(
            model_name='admin',
            name='admin_code',
            field=models.CharField(default='cFJwQYwnuQINZt13oKZUl', max_length=50),
        ),
    ]