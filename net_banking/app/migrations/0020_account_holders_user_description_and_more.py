# Generated by Django 5.0.6 on 2024-06-15 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_alter_userloandetails_loan_purpose_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='account_holders',
            name='user_description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='userloandetails',
            name='loan_description',
            field=models.TextField(default=''),
        ),
    ]
