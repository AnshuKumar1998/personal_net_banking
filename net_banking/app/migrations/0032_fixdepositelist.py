# Generated by Django 5.0.6 on 2024-06-20 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0031_alter_account_holders_profile_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='FixDepositeList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fix_deposite_id', models.CharField(editable=False, max_length=100, unique=True)),
                ('fix_deposite_name', models.CharField(max_length=100)),
                ('fix_deposite_rate_of_intrest', models.FloatField()),
                ('fix_deposite_description', models.TextField()),
                ('fix_deposite_minimum_amt', models.FloatField()),
                ('fix_deposite_maximum_amt', models.FloatField()),
            ],
        ),
    ]