# Generated by Django 5.0.7 on 2024-07-21 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0047_atmcardmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='atmcardmodel',
            name='account_no',
            field=models.IntegerField(default=0),
        ),
    ]
