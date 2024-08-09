# help.py
import shutil
from datetime import datetime, timedelta
import random
import pytz
from dateutil.relativedelta import relativedelta
from django.http import HttpResponse

from .models import UserLoanDetails, Account_Details, User_Inbox, UserTransactionDetails,ATMCardModel,TransactionSetByOtp
from django.utils import timezone
import string
import base64
import os
from django.conf import settings
from django.core.files.base import ContentFile


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

def generate_unique_transactionByOtp_id():
    while True:
        # Generate random 6-digit number (adjust as needed)
        transactionbyotp_id = random.randint(100000, 999999)  # Random number between 100000 and 999999

        # Check if loan ID already exists in database
        if not TransactionSetByOtp.objects.filter(transactionbyotp_id=transactionbyotp_id).exists():
            return transactionbyotp_id

def generate_otp(length=6):
    """Generate a unique OTP consisting of numbers and letters."""
    characters = string.ascii_uppercase + string.digits
    otp = ''.join(random.choice(characters) for _ in range(length))
    return otp


def convert_base64_to_image(base64_string, filename):
    try:
        # Check if the base64 string includes the format prefix
        if ';base64,' in base64_string:
            format, imgstr = base64_string.split(';base64,')
            ext = format.split('/')[-1]
        else:
            # Default to jpg if no format is provided
            imgstr = base64_string
            ext = 'jpg'

        img_data = base64.b64decode(imgstr)

        # Create the user folder path
        user_folder_path = os.path.join(settings.MEDIA_ROOT, 'user_login_data', filename)

        # Create the directory if it does not exist
        os.makedirs(user_folder_path, exist_ok=True)

        # Create the file path
        file_path = os.path.join(user_folder_path, f"{filename}.{ext}")

        # Save the image file
        with open(file_path, "wb") as fh:
            fh.write(img_data)

        return file_path
    except Exception as e:
        print(f"Error saving base64 image: {e}")
        return None


def convert_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        base64_encoded = base64.b64encode(image_data)
        return base64_encoded.decode('utf-8')

def del_folder(base_directory):

    base_directory = base_directory

    if os.path.exists(base_directory):
        for item in os.listdir(base_directory):
            item_path = os.path.join(base_directory, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
        return HttpResponse(f"All contents deleted from {base_directory}")
    else:
        return HttpResponse("Directory does not exist")