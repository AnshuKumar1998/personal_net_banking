# help.py

from datetime import datetime
import random
import pytz
from dateutil.relativedelta import relativedelta
from .models import UserLoanDetails, Account_Details  # Adjust accordingly based on your project structure

def kolkata_date():
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
