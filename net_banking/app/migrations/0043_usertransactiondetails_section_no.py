# Generated by Django 5.0.6 on 2024-06-24 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0042_rename_loan_id_usertransactiondetails_section'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertransactiondetails',
            name='section_no',
            field=models.CharField(default='', max_length=200),
        ),
    ]