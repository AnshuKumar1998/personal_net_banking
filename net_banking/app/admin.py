from django.contrib import admin
# Register your models here.
from .models import Contact_us, Account_holders, Account_Details, User_Inbox, MonthlyProfit, UserLoanDetails, \
    UserTransactionDetails, BankWallet, FixDepositeList, FixDepositeUsers, Post, AdminMessage,Complaint,CustomerListAccountModel, ATMCardModel,ActionCenterModel, \
TransactionSetByOtp
from django.contrib import messages






admin.site.register(Complaint)
admin.site.register(Contact_us)
admin.site.register(Account_Details)
admin.site.register(User_Inbox)
admin.site.register(MonthlyProfit)
admin.site.register(FixDepositeUsers)
admin.site.register(CustomerListAccountModel)
admin.site.register(ATMCardModel)
admin.site.register(ActionCenterModel)
admin.site.register(TransactionSetByOtp)



admin.site.register(BankWallet)
class AccountHoldersAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'mobile', 'active_loans_count','account_status')
    list_filter = ('account_status',)

admin.site.register(Account_holders, AccountHoldersAdmin)

class UserLoanDetailsAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'loan_principle_amt', 'loan_status', 'loan_release_date','loan_close_date')
    list_filter = ('email', 'username', 'loan_status', 'loan_release_date', 'loan_principle_amt','loan_close_date')
    search_fields = ('email', 'username')  # Enable search on email and username fields

    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except Exception as e:
            messages.error(request, f'Error saving loan details: {e}')
            return

        if hasattr(obj, 'update_status_success'):
            if obj.update_status_success:
                self.message_user(request, f'The loan Id {obj.loan_id} and amount {obj.loan_principle_amt} successfully transferred.')
            else:
                self.message_user(request,
                                  f'Insufficient balance in bank wallet. The loan {obj.loan_id} status was not updated.',
                                  messages.ERROR)


admin.site.register(UserLoanDetails, UserLoanDetailsAdmin)


class UserTransactionDetailsAdmin(admin.ModelAdmin):
    list_filter = ('payment_status',)
    search_fields = ('transaction_id',)  # Enable search on email and username fields

admin.site.register(UserTransactionDetails, UserTransactionDetailsAdmin)


@admin.register(FixDepositeList)
class FixDepositeListAdmin(admin.ModelAdmin):
    list_display = ('fix_deposite_id', 'fix_deposite_name', 'fix_deposite_rate_of_intrest', 'fix_deposite_minimum_amt', 'fix_deposite_maximum_amt')
    readonly_fields = ('fix_deposite_id',)


admin.site.register(Post)


@admin.register(AdminMessage)
class AdminMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'created_at', 'last_updated', 'is_active')
    list_filter = ('created_at', 'last_updated', 'is_active')
    search_fields = ('message',)
    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    make_active.short_description = "Activate selected messages"

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    make_inactive.short_description = "Deactivate selected messages"