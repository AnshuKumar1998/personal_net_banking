# Generated by Django 5.0.7 on 2024-07-31 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0060_transactionsetbyotp_transaction_action_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actioncentermodel',
            name='status',
            field=models.CharField(choices=[('new', 'New Action'), ('pending', 'Pending Action'), ('completed', 'Completed Action'), ('inactive', 'Inactive Action')], max_length=10),
        ),
    ]
