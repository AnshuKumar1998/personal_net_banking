from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver



# Create your models here.

class Contact_us(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.email

class Account_holders(models.Model):
    status = (('Running','Running'),('Blocked','Blocked'))
    status2 = (('Active','Active'),('Inactive','Inactive'))
    user = models.OneToOneField(User, on_delete=models.CASCADE,default='')
    username = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15, unique=True)
    dob = models.DateField(default='')
    address = models.TextField()
    password = models.CharField(max_length=100)
    account_status = models.CharField(choices=status2,max_length=20,default='Inactive')
    user_status = models.CharField(choices=status,default='Running',max_length=20)
    user_description = models.TextField(default='')

    def __str__(self):
        return self.email

class Account_Details(models.Model):
    user = models.OneToOneField(Account_holders, on_delete=models.CASCADE, related_name='account_details')
    username = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15, unique=True)
    upi_no = models.CharField(max_length=100)
    account_no = models.CharField(max_length=20)
    current_amt = models.IntegerField()
    pan_no = models.CharField(max_length=20)
    last_login = models.DateTimeField()
    aadhar_no = models.IntegerField()

    def __str__(self):
        return self.email


@receiver(post_delete, sender=Account_Details)
def update_account_status_on_delete(sender, instance, **kwargs):
    account_holder = instance.user
    account_holder.account_status = 'Inactive'
    account_holder.save()


class User_Inbox(models.Model):
    user = models.ForeignKey(Account_holders, on_delete=models.CASCADE, related_name='user_inboxes')
    username = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    subject = models.CharField(max_length=50)
    content = models.CharField(max_length=200)
    date = models.DateField()

    def __str__(self):
        return self.email


class MonthlyProfit(models.Model):
    month = models.CharField(max_length=20)
    profit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.month} - {self.profit}"


class UserLoanDetails(models.Model):
    status = (('Running', 'Running'),('Renewal', 'Renewal'),('Processing', 'Processing'),('Hold', 'Hold'), ('Closed', 'Closed'), ('Cancel', 'Cancel'))
    status2 = (('Business', 'Business'), ('Study', 'Study'), ('Investment', 'Investment'), ('Other', 'Other'))
    user = models.ForeignKey(Account_Details, on_delete=models.CASCADE, related_name='Account_Details')
    username = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    loan_principle_amt = models.FloatField()
    loan_paid_amt = models.FloatField(default=0.0)
    loan_purpose = models.CharField(choices=status2,max_length=20)
    loan_period = models.FloatField()
    loan_release_date = models.DateField()
    loan_close_date = models.DateField()
    loan_id = models.CharField(max_length=20)
    loan_intrest_rate = models.FloatField()
    loan_returing_amt = models.FloatField()
    loan_fine_amt = models.FloatField()
    loan_status = models.CharField(choices=status,max_length=20)
    loan_renewal_times = models.IntegerField()
    loan_refrence_code = models.CharField(max_length=20)
    loan_description = models.TextField(default='')

    def __str__(self):
        return f"{self.email} - {self.loan_principle_amt} - {self.loan_status}"


class UserTransactionDetails(models.Model):
    user = models.ForeignKey(Account_holders, on_delete=models.CASCADE, related_name='transactions')
    username = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    transaction_id = models.CharField(max_length=100)  # Unique transaction identifier
    transaction_date = models.DateTimeField(auto_now_add=True)  # Date and time of the transaction
    transaction_type = models.CharField(max_length=50)  # Type of transaction (e.g., 'payment', 'refund')
    loan_id = models.CharField(max_length=100, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount of the transaction
    payment_method = models.CharField(max_length=50)  # Payment method (e.g., 'credit card', 'bank transfer')
    payment_status = models.CharField(max_length=50)  # Status of the payment (e.g., 'completed', 'pending', 'failed')
    description = models.TextField(null=True, blank=True)  # Additional details about the transaction
    class Meta:
        ordering = ['-transaction_date']  # Orders transactions by date, most recent first

    def __str__(self):
        return f'Transaction {self.transaction_id} by {self.username}'

class BankWallet(models.Model):
    bank_amount = models.FloatField(default=0.0)
    update_date = models.DateField(auto_now=True)
    description = models.TextField(null=True, blank=True)  # Additional details about the transaction

    def save(self, *args, **kwargs):
        if not self.pk and BankWallet.objects.exists():
            raise Exception('There can be only one BankWallet instance')
        return super(BankWallet, self).save(*args, **kwargs)

    @classmethod
    def get_instance(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            instance = cls()
            instance.save()
            return instance

    def __str__(self):
        return str(self.bank_amount)