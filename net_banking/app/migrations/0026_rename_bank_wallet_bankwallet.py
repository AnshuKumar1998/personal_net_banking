# Generated by Django 5.0.6 on 2024-06-17 08:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_alter_bank_wallet_bank_amount'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='bank_wallet',
            new_name='BankWallet',
        ),
    ]
