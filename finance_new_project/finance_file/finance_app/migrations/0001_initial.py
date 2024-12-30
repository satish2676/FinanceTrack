# Generated by Django 5.1.3 on 2024-12-02 06:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin_name', models.CharField(default='s', max_length=100)),
                ('admin_mobile', models.CharField(max_length=10, unique=True)),
                ('admin_password', models.CharField(max_length=20)),
                ('admin_code', models.CharField(default='satish123')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_id', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=100)),
                ('mobile', models.CharField(max_length=10)),
                ('loan_disberment_amount', models.IntegerField()),
                ('loan_date', models.DateField(auto_now_add=True)),
                ('address', models.TextField()),
                ('paid_amount', models.IntegerField()),
                ('today_date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid_date', models.DateField()),
                ('is_paid', models.BooleanField(default=False)),
                ('today_date', models.DateField(auto_now=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance_app.member')),
            ],
        ),
    ]