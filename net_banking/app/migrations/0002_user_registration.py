# Generated by Django 5.0.6 on 2024-06-09 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('gender', models.CharField(max_length=6)),
                ('mobile', models.CharField(max_length=11)),
                ('date_of_birth', models.DateField()),
                ('password', models.CharField(max_length=20)),
                ('address', models.TextField()),
            ],
        ),
    ]
