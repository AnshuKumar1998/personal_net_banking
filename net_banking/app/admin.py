from django.contrib import admin

# Register your models here.

from .models import Contact_us,Account_holders,Account_Details

admin.site.register(Contact_us)
admin.site.register(Account_holders)
admin.site.register(Account_Details)