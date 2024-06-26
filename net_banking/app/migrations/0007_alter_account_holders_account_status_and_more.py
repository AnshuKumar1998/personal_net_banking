# Generated by Django 5.0.6 on 2024-06-13 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_account_holders_account_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account_holders',
            name='account_status',
            field=models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Inactive', max_length=20),
        ),
        migrations.AlterField(
            model_name='account_holders',
            name='user_status',
            field=models.CharField(choices=[('Running', 'Running'), ('Blocked', 'Blocked')], default='Running', max_length=20),
        ),
    ]
