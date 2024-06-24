# Generated by Django 5.0.6 on 2024-06-23 03:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0039_rename_complaint_id_complaint_complaint_id_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='userloandetails',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Account_Details', to=settings.AUTH_USER_MODEL),
        ),
    ]
