# Generated by Django 5.0.6 on 2024-06-20 09:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0033_fixdepositelist_fix_deposite_month'),
    ]

    operations = [
        migrations.CreateModel(
            name='FixDepositeUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('mobile', models.CharField(max_length=15)),
                ('fix_deposite_id', models.CharField(max_length=100)),
                ('fix_deposite_name', models.CharField(max_length=100)),
                ('fix_deposite_rate_of_intrest', models.FloatField()),
                ('fix_deposite_month', models.FloatField(default=0)),
                ('fix_deposite_amt', models.FloatField()),
                ('fix_deposite_maturity_amt', models.FloatField()),
                ('fix_deposite_st_date', models.DateField()),
                ('fix_deposite_end_date', models.DateField()),
                ('fix_deposite_status', models.CharField(choices=[('Running', 'Running'), ('Processing', 'Processing'), ('Hold', 'Hold'), ('Closed', 'Closed'), ('Cancel', 'Cancel')], max_length=100)),
                ('fix_deposite_description', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fixDeposite', to='app.account_holders')),
            ],
            options={
                'ordering': ['-fix_deposite_st_date'],
            },
        ),
    ]
