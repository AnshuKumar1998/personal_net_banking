# Generated by Django 5.0.6 on 2024-06-18 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0030_account_holders_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account_holders',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to='upload_profile_photo/'),
        ),
    ]