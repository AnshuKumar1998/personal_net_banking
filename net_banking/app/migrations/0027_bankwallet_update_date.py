# Generated by Django 5.0.6 on 2024-06-17 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_rename_bank_wallet_bankwallet'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankwallet',
            name='update_date',
            field=models.DateField(auto_now=True),
        ),
    ]