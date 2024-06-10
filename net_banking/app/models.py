from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create your models here.

class Contact_us(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.email

class Account_holders(models.Model):

    username = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15, unique=True)
    dob = models.DateField()
    address = models.TextField()
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name



