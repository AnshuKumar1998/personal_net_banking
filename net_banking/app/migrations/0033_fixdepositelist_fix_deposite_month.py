# Generated by Django 5.0.6 on 2024-06-20 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_fixdepositelist'),
    ]

    operations = [
        migrations.AddField(
            model_name='fixdepositelist',
            name='fix_deposite_month',
            field=models.FloatField(default=0),
        ),
    ]
