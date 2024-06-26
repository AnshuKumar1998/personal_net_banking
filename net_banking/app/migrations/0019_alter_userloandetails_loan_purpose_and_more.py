# Generated by Django 5.0.6 on 2024-06-15 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_alter_userloandetails_loan_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userloandetails',
            name='loan_purpose',
            field=models.CharField(choices=[('Business', 'Business'), ('Study', 'Study'), ('Investment', 'Investment'), ('Other', 'Other')], max_length=20),
        ),
        migrations.AlterField(
            model_name='userloandetails',
            name='loan_status',
            field=models.CharField(choices=[('Running', 'Running'), ('Renewal', 'Renewal'), ('Processing', 'Processing'), ('Hold', 'Hold'), ('Closed', 'Closed'), ('Cancel', 'Cancel')], max_length=20),
        ),
    ]
