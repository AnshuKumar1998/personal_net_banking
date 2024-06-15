from django.contrib import admin
# Register your models here.
from .models import Contact_us,Account_holders,Account_Details,User_Inbox,MonthlyProfit,UserLoanDetails

admin.site.register(Contact_us)
admin.site.register(Account_holders)
admin.site.register(Account_Details)
admin.site.register(User_Inbox)
admin.site.register(MonthlyProfit)
admin.site.register(UserLoanDetails)