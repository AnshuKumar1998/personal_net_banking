# help.py

from datetime import datetime, timedelta
import random
import pytz
from dateutil.relativedelta import relativedelta
from .models import UserLoanDetails, Account_Details, User_Inbox, UserTransactionDetails,ATMCardModel
from django.utils import timezone


def today_date():
    kolkata_timezone = pytz.timezone('Asia/Kolkata')
    kolkata_time = datetime.now(kolkata_timezone)
    return kolkata_time.date()

def generate_unique_loan_id():
    while True:
        # Generate random 6-digit number (adjust as needed)
        loan_id = random.randint(100000, 999999)  # Random number between 100000 and 999999

        # Check if loan ID already exists in database
        if not UserLoanDetails.objects.filter(loan_id=loan_id).exists():
            return loan_id

def calculate_due_date(loan_period_months):
    kolkata_timezone = pytz.timezone('Asia/Kolkata')
    current_kolkata_time = datetime.now(kolkata_timezone)
    due_date = current_kolkata_time + relativedelta(months=loan_period_months)
    due_date = due_date.date()  # Extract the date part

    return due_date

def generate_unique_account_number():
    while True:
        # Generate random 8-digit number
        account_number = random.randint(10000000, 99999999)  # Random number between 10000000 and 99999999

        # Check if account number already exists in database
        if not Account_Details.objects.filter(account_no=account_number).exists():
            return account_number


def today_date_time():
    kolkata_timezone = pytz.timezone('Asia/Kolkata')
    kolkata_time = datetime.now(kolkata_timezone)
    formatted_date_time = kolkata_time.strftime('%Y-%m-%d %I:%M %p')
    return formatted_date_time

def inbox_message(account_holder, subject, content):
    formatted_date_time_str = today_date_time()
    date_obj = datetime.strptime(formatted_date_time_str, '%Y-%m-%d %I:%M %p')
    User_Inbox.objects.create(
        user=account_holder,
        username=account_holder.username,
        name=account_holder.name,
        email=account_holder.email,
        mobile=account_holder.mobile,
        subject=subject,
        content=content,
        date=date_obj
    )



def transaction_slip(account_holder,transaction_id,withdraw,section,section_no,amount,method,status):
      # Replace with actual logic
    UserTransactionDetails.objects.create(
        user=account_holder,
        username=account_holder.username,
        name=account_holder.name,
        email=account_holder.email,
        mobile=account_holder.mobile,
        transaction_id=transaction_id,
        transaction_date=datetime.now(),
        transaction_type=withdraw,
        section=section,
        section_no=section_no,
        amount=amount,
        payment_method=method,
        payment_status=status,
        description=""
    )


def generate_unique_card_number():
    while True:
        card_number = ''.join([str(random.randint(0, 9)) for _ in range(16)])
        if not ATMCardModel.objects.filter(card_number=card_number).exists():
            return card_number

def generate_cvv():
    return ''.join([str(random.randint(0, 9)) for _ in range(3)])

def generate_pin():
    return ''.join([str(random.randint(0, 9)) for _ in range(4)])
def create_atm_card(account_holder, account_details):

    username = account_holder.username
    name = account_holder.name
    email = account_holder.email
    account_no = account_details.account_no
    cardholder_name = account_holder.name
    pin = generate_pin()
    card_number = generate_unique_card_number()
    cvv = generate_cvv()
    expiration_date = timezone.now().date() + timedelta(days=5*365)  # 5 years from today

    atm_card = ATMCardModel(
        user=account_details,
        username=username,
        name=name,
        email=email,
        account_no=account_no,
        card_number=card_number,
        cardholder_name=cardholder_name,
        expiration_date=expiration_date,
        cvv=cvv,
        pin=pin
    )
    atm_card.save()

    return True # Replace with your success URL

