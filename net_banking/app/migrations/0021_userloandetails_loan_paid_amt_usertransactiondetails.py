# Generated by Django 5.0.6 on 2024-06-16 10:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_account_holders_user_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userloandetails',
            name='loan_paid_amt',
            field=models.FloatField(default=0.0),
        ),
        migrations.CreateModel(
            name='UserTransactionDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('mobile', models.CharField(max_length=15)),
                ('transaction_id', models.CharField(max_length=100, unique=True)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('transaction_type', models.CharField(max_length=50)),
                ('loan_id', models.CharField(blank=True, max_length=100, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_method', models.CharField(max_length=50)),
                ('payment_status', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='app.account_holders')),
            ],
            options={
                'ordering': ['-transaction_date'],
            },
        ),
    ]
