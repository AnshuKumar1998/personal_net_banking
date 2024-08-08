import base64
import os
import uuid
import json
from django.conf import settings
from django.core.files.storage import default_storage
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.db.models import F, ExpressionWrapper, FloatField, Q
from django.http import JsonResponse, HttpResponse
from app.models import Contact_us,Account_holders,Account_Details,User_Inbox,MonthlyProfit,UserLoanDetails,UserTransactionDetails,BankWallet,FixDepositeList,FixDepositeUsers,Post,AdminMessage,Complaint,CustomerListAccountModel, ATMCardModel,ActionCenterModel,TransactionSetByOtp
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from app.help import today_date, generate_unique_loan_id, calculate_due_date, generate_unique_account_number, inbox_message,transaction_slip, create_atm_card,generate_otp,today_date_time,generate_unique_transactionByOtp_id,convert_base64_to_image,convert_image_to_base64
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import logging
from django.core.paginator import Paginator
from django.contrib.auth.hashers import check_password
from django.views.decorators.http import require_POST, require_http_methods
from django.db.models import Count
from django.core.mail import EmailMessage
from io import BytesIO
from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from django.utils.dateformat import format
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)




#---------------------Website Page-----------------------
def master(request):
    return render(request,'master.html')

def index(request):
    user_count = Account_holders.objects.count()
    bank_wallet = BankWallet.get_instance()
    current_amount = bank_wallet.bank_amount if bank_wallet else 0.0
    account_count = Account_Details.objects.count()
    context = {
        'user_count': user_count,
        'current_deposite':current_amount,
        'account_count':account_count
    }
    return render(request,'index.html',context)

def blog(request):
    return render(request,'users_dir/blog.html')

def contact_us(request):
    if request.method == "POST":

        contact = Contact_us(
            name = request.POST.get('name'),
            email = request.POST.get('email'),
            message = request.POST.get('message')
        )
        contact.save()
        messages.success(request, 'Your message has been successfully sent!')
        return redirect('contact_us')  # Prevent form resubmission

    name = "None"
    if request.user.is_authenticated:
        profile_holder = get_object_or_404(Account_holders, user=request.user)
        name = profile_holder.name
    context = {
        'name':name
    }
    return render(request,'contact_us.html',context)


def service(request):
    name = "None"
    if request.user.is_authenticated:
        profile_holder = get_object_or_404(Account_holders, user=request.user)
        name = profile_holder.name
    context = {
        'name': name
    }
    return render(request, 'service_dir/service.html',context)

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('user_account')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'users_dir/login.html')

    return render(request, 'users_dir/login.html')

def post_list(request):
    name="none"
    if request.user.is_authenticated:
        profile_holder = get_object_or_404(Account_holders, user=request.user)
        name = profile_holder.name

    posts = Post.objects.all().order_by('-date')
    paginator = Paginator(posts, 5)  # Show 5 posts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context ={
        'page_obj':page_obj,
        'name':name
    }
    return render(request, 'post_list.html', context)

@csrf_exempt
def like_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        post.likes += 1
        post.save()
        return JsonResponse({'likes': post.likes})

#---------------------End Website Page-----------------------




#---------------------user account-----------------------
@never_cache
@login_required
def user_account(request):
    try:
        profile = Account_holders.objects.get(user=request.user)

        try:
            account_data = Account_Details.objects.get(username=profile.username)
        except Account_Details.DoesNotExist:
            account_data = None

        loan_data = UserLoanDetails.objects.filter(username=profile.username).annotate(
            total=ExpressionWrapper(
                F('loan_returing_amt') - F('loan_paid_amt'),
                output_field=FloatField()
            )
        ).order_by('-loan_release_date')

        user_messages = User_Inbox.objects.filter(username=profile.username).order_by('-date')

        bank_wallet = BankWallet.get_instance()
        current_amount = bank_wallet.bank_amount if bank_wallet else 0.0

        now = timezone.now()
        active_admin_message = "true"

        image_path=""

        if profile.photo:
            base64_string = profile.photo
            filename = profile.username

            image_return =convert_base64_to_image(base64_string, filename)
            if image_return:
                image_path = "/" + image_return
            else:
                image_path=""
            profile.profile_photo = image_path
            profile.save()


        transactions = UserTransactionDetails.objects.filter(username=request.user).order_by('-transaction_date')
        transaction_list = list(transactions.values(
            'section',
            'amount',
            'transaction_type',
            'transaction_id',
            'payment_status',
            'payment_method',
            'transaction_date'
        ))

        profile_data = {
            'name': profile.name,
            'username': profile.username,
            'gender': profile.gender,
            'mobile': profile.mobile,
            'email': profile.email,
            'dob': profile.dob,
            'address': profile.address,
            'user_account': profile.account_status,
            'user_status': profile.user_status,
            'account_no': account_data.account_no if account_data else None,
            'upi_no': account_data.upi_no if account_data else None,
            'current_amt': account_data.current_amt if account_data else None,
            'pan_no': account_data.pan_no if account_data else None,
            'aadhar_no': account_data.aadhar_no if account_data else None,
            'last_login': account_data.last_login if account_data else None,
            'messages': user_messages,
            'loan_details': loan_data,
            'transactions': transaction_list,
            'bank_amount': current_amount,
            'show_message': active_admin_message,
            'image_path': image_path
        }

    except Account_holders.DoesNotExist:
        profile_data = {}
        messages.error(request, 'User account not found.')

    context = {
        'profile_data': profile_data,
    }

    return render(request, 'users_dir/user_account.html', context)


def logout(request):

    auth_logout(request)
    response = redirect('login')
    response.delete_cookie('sessionid')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'

    return response

def new_account_holder(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        dob = request.POST.get('dob')
        address = request.POST.get('address')
        password = request.POST.get('password')
       # profile_photo = request.FILES.get('profile_photo')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Error: This email is already registered.')
        elif Account_holders.objects.filter(mobile=mobile).exists():
            messages.error(request, 'Error: This mobile number is already registered.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Error: This username is already registered.')
        else:
            # Convert the image file to base64

            user = User(username=username, email=email, password=make_password(password))
            user.save()
            profile = Account_holders.objects.create(
                user=user,
                username=username,
                name=name,
                email=email,
                gender=gender,
                mobile=mobile,
                dob=dob,
                password=password,
                address=address,

            )
            profile.save()
            inbox_message(profile, "Welcome to Our Service", "Thank you for creating an account with us.")
            messages.success(request, 'Your Account Has Been Created successfully!')
            return redirect('signup')

    return render(request, 'users_dir/signup.html')

@login_required
def activate(request):
    if request.method == 'POST':
        pan_no = request.POST.get('pancard')
        aadhar_no = request.POST.get('aadharno')


        # Check if PAN number or Aadhar number already exists
        if Account_Details.objects.filter(pan_no=pan_no).exists():
            messages.error(request, 'PAN number already exists')
            return redirect('user_account')
        elif Account_Details.objects.filter(aadhar_no=aadhar_no).exists():
            messages.error(request, 'Aadhar number already exists')
            return redirect('user_account')

        # Assuming form data is validated and cleaned
        account_holder = Account_holders.objects.get(user=request.user)
        dob_str = account_holder.dob

        if isinstance(dob_str, str):
            dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
        else:
            dob = dob_str

            # Calculate the user's age
        today = datetime.today().date()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if age < 18:
            messages.error(request, 'You must be at least 18 years old')
            return redirect('user_account')

        account_details = Account_Details.objects.create(
            name=account_holder.name,
            username=account_holder.username,
            mobile=account_holder.mobile,
            email=account_holder.email,
            user=account_holder,
            upi_no=account_holder.mobile + '@mini',
            account_no=generate_unique_account_number(),
            current_amt=0,
            pan_no=request.POST['pancard'],
            last_login= timezone.now(),
            aadhar_no=request.POST['aadharno']
        )
        create_atm_card(account_holder,account_details)
        account_holder.account_status = 'Active'  # Example: Updating account_status column
        account_holder.save()
        inbox_message(account_holder,"Account Activation","Your account has been successfully activated.")
        messages.success(request, 'Account Successfully Activated')
        return redirect('user_account')

    return render(request, 'users_dir/user_account.html')

@login_required
def update_profile(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        dob = request.POST.get('dob')

        account_holder = Account_holders.objects.get(user=request.user)
        account_holder.name = name
        account_holder.gender = gender
        account_holder.address = address
        account_holder.dob = dob
        account_holder.save()
        inbox_message(account_holder,"Profile Update","Your profile has been successfully Updated.")
        messages.success(request, 'Profile Successfully Updated')  #
        return redirect('user_account')
    return render(request, 'users_dir/user_account.html')

def get_profit_data(request):
    data = MonthlyProfit.objects.all().values('month', 'profit')
    return JsonResponse(list(data), safe=False)

@login_required
def chart_view(request):
    return render(request, 'users_dir/blog.html')

@login_required
def user_setting(request):
    profile = Account_holders.objects.get(username = request.user.username)
    context = {
        'name':profile.name,
    }
    return render(request,'user_setting_dir/user_setting.html',context)

@login_required
def user_activity(request):
    user = request.user
    profile = Account_holders.objects.get(username=user)
    statuses = ['Running', 'Processing', 'Hold']
    loans = UserLoanDetails.objects.filter(username=profile.username).filter(Q(loan_status='Running') | Q(loan_status='Processing') | Q(loan_status='Hold'))
    fix_deposites = FixDepositeUsers.objects.filter(username=profile.username)

    user_profile = {
        "name":profile.name
    }
    context = {
        'profile': user_profile,
        "loans":loans,
        "fix_deposites":fix_deposites,

    }
    return render(request, 'user_setting_dir/user_activity.html', context)


def complaint_form(request):
    profile_holder = get_object_or_404(Account_holders, user=request.user)
    if request.method == "POST":
        name = profile_holder.name
        email = profile_holder.email
        message = request.POST.get('message')
        file = request.FILES.get('formFile')

        complaint_id = str(uuid.uuid4())

        complaint = Complaint(
            name=name,
            email=email,
            message=message,
            file=file,
            complaint_id=complaint_id
        )
        complaint.save()

        inbox_message(profile_holder, "Complaint", f"Complaint has been sent successfully.")

        messages.success(request, 'Your complaint has been successfully sent!')
        return redirect(reverse('complaint_form'))

    recent_complaints = Complaint.objects.filter(email=profile_holder.email).order_by('-created_at')

    context = {
        'name': profile_holder.name,
        'email': profile_holder.email,
        'recent_complaints': recent_complaints,
    }

    return render(request, 'user_complaint.html', context)

def delete_complaint(request, id):
    if request.method == 'POST':
        complaint = get_object_or_404(Complaint, id=id)
        complaint.delete()
        messages.success(request, 'Complaint deleted successfully.')
    return redirect('complaint_form')  # Adjust 'complaint_page' to your actual complaint listing page name


@csrf_exempt  # Temporarily exempt CSRF to focus on troubleshooting
def transfer_money(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            account = data.get('account')
            amount = float(data.get('amount'))

            user_account = Account_Details.objects.get(username=request.user.username)
            atm_details = ATMCardModel.objects.get(account_no=user_account.account_no)
            account_holder = Account_holders.objects.get(username=request.user.username)
            user_name = account_holder.name


            # Example: Perform money transfer logic here
            if atm_details.net_banking_service:
                if user_account.current_amt >= amount:
                    # Deduct amount from current user's balance
                    user_account.current_amt -= amount
                    user_account.save()

                    transaction_slip(account_holder, 000, "Debited", "Transfer", account, amount, "Account","Complete")
                    inbox_message(account_holder, "Money Transfer", f"Your money of {amount} has been successfully transferred.")

                    # Add amount to recipient's account
                    try:
                        recipient = Account_Details.objects.get(account_no=account)
                        recipient.current_amt += amount
                        recipient.save()

                        recipient_account_holder = Account_holders.objects.get(username=recipient.username)
                        transaction_slip(recipient_account_holder, 000, "Credited", "Recived", account, amount, "Account", "Success")

                        inbox_message(recipient_account_holder, "Credited Money", f"{user_name} sent {amount} to your account")

                       # messages.success(request, 'Money transferred successfully.')
                        return JsonResponse({'message': 'Money transferred successfully.'})

                    except Account_Details.DoesNotExist:
                        #messages.error(request, 'Recipient account not found.')
                        return JsonResponse({'message': 'Recipient account not found.'})

                else:
                    #messages.error(request, 'Insufficient balance to transfer money.')
                    return JsonResponse({'message': 'Insufficient balance to transfer money.'}, status=400)
            else:
                return JsonResponse({'message': 'Net Banking Service is Disable.'}, status=404)

        except Exception as e:
            #messages.error(request, f'Error: {str(e)}')
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Method not allowed.'}, status=405)

def fetch_user_data(request):
    if request.method == 'GET':
        account_input = request.GET.get('accountInput')

        if account_input.isdigit():
            account_details = get_object_or_404(Account_Details, account_no=account_input)
        else:
            account_details = get_object_or_404(Account_Details, upi_no=account_input)

        user_data = {
            'name': account_details.name,
            'email': account_details.email,
            'mobile': account_details.mobile,
        }


        if user_data:
            return JsonResponse({'success': True, 'data': user_data})
        else:
            return JsonResponse({'success': False})

    return render(request, 'users_dir/user_account.html')


@login_required
def verify_old_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        old_password = data.get('old_password')

        if check_password(old_password, request.user.password):
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Old password is incorrect'})
@login_required
def change_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_password = data.get('new_password')

        account_holder = Account_holders.objects.get(user=request.user)

        account_holder.password = new_password
        account_holder.save()

        user = request.user
        user.set_password(new_password)
        user.save()

        update_session_auth_hash(request, user)  # Prevents user from being logged out after password change
        inbox_message(account_holder, "Password Changed","Your Password Successfully has been changed")
        messages.success(request, 'Password changed successfully.')
        return JsonResponse({'status': 'success'})

    messages.error(request, 'Failed to change password.')
    return JsonResponse({'status': 'error', 'message': 'Failed to change password.'})


@csrf_exempt
@require_POST
def update_amount(request):
    data = json.loads(request.body)
    amount = float(data.get('amount'))
    profile_holder = get_object_or_404(Account_holders, user=request.user)

    if amount < 99:
        inbox_message(profile_holder, "Failed Credited Money", f"Money Rs. {amount} Failed credited to your account")
        return JsonResponse({'success': False, 'message': 'Failed to add money.'})

    if amount is not None:

        profile_data = get_object_or_404(Account_Details, username=profile_holder.username)

        # Update current amount
        profile_data.current_amt += amount
        profile_data.save()
        transaction_slip(profile_holder, 000, "Credited", "Add Money", "self", amount, "Credit Card", "Complete")

        # Send inbox message
        inbox_message(profile_holder, "Credited Money", f"Money Rs. {amount} Successfully credited to your account")

        # Return JsonResponse with success message and updated amount
        return JsonResponse({'success': True, 'message': 'Money added successfully.', 'new_amount': profile_data.current_amt})

    return JsonResponse({'success': False, 'message': 'Failed to add money.'})

def get_current_amount(request):
    profile_holder = get_object_or_404(Account_holders, user=request.user)
    profile_data = get_object_or_404(Account_Details, username=profile_holder.username)
    return JsonResponse({'success': True, 'current_amount': profile_data.current_amt})


#---------------------End user account-----------------------



#---------------------Inbox-----------------------

@csrf_exempt
def delete_message(request, message_id):
    if request.method == 'DELETE':
        try:
            message = User_Inbox.objects.get(id=message_id)
            message.delete()
            return JsonResponse({'success': True})
        except User_Inbox.DoesNotExist:
            return JsonResponse({'error': 'Message not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)

#---------------------End Inbox-----------------------




# ---------------------  loan Related All Function Here-----------------------
@login_required
def loan_preview_form(request):
    if request.method == "POST":
        # Get form inputs
        loan_amt = float(request.POST.get("loan_amt"))  # Convert to float

        bank_wallet = BankWallet.get_instance()

        if bank_wallet:
            # Get the current bank amount
            current_amount = bank_wallet.bank_amount

            if loan_amt>current_amount:
                messages.error(request, 'Sufficent Balance')
                return redirect('user_account')

        loan_purpose = request.POST.get("purpose")
        loan_period = float(request.POST.get("loan_period"))  # Convert to float
        loan_refrence_code = request.POST.get("reference_no")

        # Calculate due date based on loan period
        due_date = calculate_due_date(int(loan_period))  # Ensure period is an integer for calculation
        loan_id = generate_unique_loan_id()
        # Define interest rate (assuming 2% per month)
        interest_rate = 0.02

        # Calculate returning amount based on simple interest formula
        loan_returning_amt = loan_amt * interest_rate * loan_period + loan_amt

        # Fetch account details for the logged-in user
        account_holder = Account_holders.objects.get(user=request.user)
        account_details = account_holder.account_details

        loan_data = {
            "name": account_details.name,
            "loan_amount":loan_amt,
            "purpose":loan_purpose,
            "release_date":today_date(),
            "close_date":due_date,
            "intrest_rate":interest_rate,
            "returning_amount":loan_returning_amt,
            "refrence_code":loan_refrence_code,
            "peroid":loan_period
        }
        context = {
            'data': loan_data,
        }

        return render(request, 'loan_preview.html', context)

    # If not a POST request, render the loan form template
    return render(request, 'users_dir/user_account.html')
@login_required
def loan_form(request):
    if request.method == "POST":
        # Get form inputs
        loan_amt = float(request.POST.get("loan_amt"))  # Convert to float

        bank_wallet = BankWallet.get_instance()

        if bank_wallet:
            # Get the current bank amount
            current_amount = bank_wallet.bank_amount

            if loan_amt>current_amount:
                messages.error(request, 'Sufficent Balance')
                return redirect('user_account')

        loan_purpose = request.POST.get("purpose")
        loan_period = float(request.POST.get("loan_period"))  # Convert to float
        loan_refrence_code = request.POST.get("reference_no")

        # Calculate due date based on loan period
        due_date = calculate_due_date(int(loan_period))  # Ensure period is an integer for calculation
        loan_id = generate_unique_loan_id()
        # Define interest rate (assuming 2% per month)
        interest_rate = 0.02

        # Calculate returning amount based on simple interest formula
        loan_returning_amt = loan_amt * interest_rate * loan_period + loan_amt

        # Fetch account details for the logged-in user
        account_holder = Account_holders.objects.get(user=request.user)
        account_details = account_holder.account_details

        # Create UserLoanDetails instance
        UserLoanDetails.objects.create(
            user=account_details,
            username=account_details.username,
            name=account_details.name,
            email=account_details.email,
            mobile=account_details.mobile,
            loan_principle_amt=loan_amt,
            loan_purpose=loan_purpose,
            loan_period=loan_period,
            loan_release_date=today_date(),
            loan_close_date=due_date,
            loan_id=loan_id,  # Generate unique loan ID
            loan_intrest_rate=interest_rate,
            loan_returing_amt=loan_returning_amt,
            loan_fine_amt=5,  # Example fine amount
            loan_status="Processing",
            loan_renewal_times=0,
            loan_refrence_code=loan_refrence_code,
        )
        bank_wallet.bank_amount -= loan_amt
        bank_wallet.update_date = today_date()
        bank_wallet.save()
        # Create User_Inbox entry
        content = f"Your Loan ₹ {loan_amt:.2f} for {loan_purpose} for {loan_period} month(s) applied.\n"
        f"You can also check the loan status through Loan Id.\nYour loan ID is: {loan_id}.\n"
        "Thank you for visiting our bank."
        inbox_message(account_holder,"Loan Request is Processing",content)


        # Display success message and redirect
        messages.success(request, 'Loan Successfully Applied')
        return redirect('user_account')

    # If not a POST request, render the loan form template
    return render(request, 'users_dir/user_account.html')

@csrf_exempt
def delete_loan(request, loan_id):
    if request.method == 'DELETE':
        try:
            loan = UserLoanDetails.objects.get(loan_id=loan_id)
            loan.delete()
            return JsonResponse({'success': True})
        except UserLoanDetails.DoesNotExist:
            return JsonResponse({'error': 'Loan not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def payment_page(request):
    loan_id = request.GET.get('loan_id')
    context = {}

    try:
        loan_details = UserLoanDetails.objects.get(loan_id=loan_id, username=request.user)
        total = (loan_details.loan_returing_amt + loan_details.loan_fine_amt) - loan_details.loan_paid_amt

        context = {
            'loan_id': loan_details.loan_id,
            'amount': loan_details.loan_principle_amt,
            'return_amount': loan_details.loan_returing_amt,
            'fine': loan_details.loan_fine_amt,
            'name': loan_details.name,
            'paid':loan_details.loan_paid_amt,
            'total': total,
        }
    except UserLoanDetails.DoesNotExist:
        messages.error(request, "You do not have permission to view this loan.")

    return render(request, 'payment_page.html', context)

@receiver(pre_save, sender=UserLoanDetails)
def update_loan_status(sender, instance, **kwargs):
    if instance.pk:
        previous = UserLoanDetails.objects.get(pk=instance.pk)
        if previous.loan_status == "Processing" and instance.loan_status == "Running":

            bank_wallet = BankWallet.get_instance()
            account_holder = Account_holders.objects.get(email=instance.user)
            account_details = Account_Details.objects.get(username=account_holder.username)

            # Check if bank balance is sufficient
            if bank_wallet.bank_amount >= instance.loan_principle_amt:
                # Subtract the loan amount from bank_wallet.bank_amount
                bank_wallet.bank_amount -= instance.loan_principle_amt
                bank_wallet.update_date = timezone.now()
                bank_wallet.save()

                # Add the loan amount to the user's account balance
                account_details.current_amt += instance.loan_principle_amt
                account_details.save()

                # Set success flag for successful update
                instance.update_status_success = True

            else:
                # Set flag for insufficient balance
                instance.update_status_success = False

@login_required
def process_payment(request):
    if request.method == "POST":
        loan_id = request.POST.get('loan_id')
        pay_amt = float(request.POST.get('pay_amt'))

        try:
            account_holder = Account_holders.objects.get(user=request.user)
            loan_details = get_object_or_404(UserLoanDetails, loan_id=loan_id, username=request.user)
            bank_wallet = BankWallet.get_instance()

            total = (loan_details.loan_returing_amt + loan_details.loan_fine_amt) - loan_details.loan_paid_amt

            with transaction.atomic():
                if pay_amt == total:
                    loan_details.loan_status = "Closed"
                    loan_details.save()
                    transaction_slip(account_holder, 000, "Debited", "Loan",loan_id, pay_amt, "Credit Card", "Complete")
                    inbox_message(account_holder, "Loan Closed",f"Your loan {pay_amt} was successfully closed.\nThank you for choosing us.")
                    bank_wallet.bank_amount += pay_amt
                    bank_wallet.update_date = today_date()
                    bank_wallet.save()
                    messages.success(request, "Loan closed successfully.")
                elif pay_amt < total:
                    remaining = total - pay_amt
                    if remaining < 100:
                        context = {
                            'loan_id': loan_details.loan_id,
                            'amount': loan_details.loan_principle_amt,
                            'return_amount': loan_details.loan_returing_amt,
                            'fine': loan_details.loan_fine_amt,
                            'name': loan_details.name,
                            'paid': loan_details.loan_paid_amt,
                            'total': total,
                        }
                        messages.error(request, "Remaining can't less then 100.")

                        return render(request,'payment_page.html',context)

                    loan_details.loan_paid_amt += pay_amt
                    loan_details.save()
                    transaction_slip(account_holder, 000, "Debited", "Loan",loan_id, pay_amt, "Credit Card", "Complete")
                    inbox_message(account_holder,"Loan Paid Transaction",f"Your payment of {pay_amt} was successful. Remaining amount: {remaining}")
                    bank_wallet.bank_amount += pay_amt
                    bank_wallet.update_date = today_date()
                    bank_wallet.save()
                    messages.success(request, f"Your payment of {pay_amt} was successful. Remaining amount: {remaining}")
                else:
                    messages.error(request, "Invalid payment amount.")

        except Account_holders.DoesNotExist:
            messages.error(request, "You do not have permission to view this account.")
        except UserLoanDetails.DoesNotExist:
            messages.error(request, "You do not have permission to view this loan.")

        return redirect('user_account')

    return redirect('user_account')
# -------------------------------End Loan Related Function-----------------------



@login_required
def hide_message(request):
    if request.method == 'POST':
        try:
            profile = Account_holders.objects.get(user=request.user)
            profile.message_seen = True
            profile.save()
            return JsonResponse({'status': 'ok'})
        except Account_holders.DoesNotExist:
            return JsonResponse({'status': 'error'})


@login_required
@csrf_exempt
def delete_account(request):
    if request.method == 'POST':
        username = request.user.username

        # Check if there are running or processing loans or fixed deposits
        running_loans = UserLoanDetails.objects.filter(username=username, loan_status__in=['Running', 'Processing'])
        running_deposits = FixDepositeUsers.objects.filter(username=username, fix_deposite_status='Running')

        if running_loans.exists() or running_deposits.exists():
            return JsonResponse({'status': 'error', 'message': "You can't delete your account with running or processing loans/deposits."})

        # Delete User Inbox data
        User_Inbox.objects.filter(username=username).delete()

        try:
            # Delete account details if they exist
            account_details = Account_Details.objects.get(username=username)
            account_details.delete()
        except Account_Details.DoesNotExist:
            pass

        # Delete account holder details
        account_holder = Account_holders.objects.get(username=username)
        account_holder.delete()

        # Delete Django User model
        try:
            user = User.objects.get(username=username)
            user.delete()
        except User.DoesNotExist:
            pass

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

# ------------------------Fix Deposite Data ------------------------------------

def fix_deposit_list(request):
    fix_deposits = FixDepositeList.objects.all()

    if request.user.is_authenticated:
        profile = Account_holders.objects.get(username=request.user)
        name=profile.name
    else:
        name="none"

    context = {
        'profile':name,
        'fix_deposits': fix_deposits

    }
    return render(request, 'service_dir/fix_deposit_list.html',context)

def fix_deposite_details(request, fix_deposite_id):

    fix_deposit = get_object_or_404(FixDepositeList, fix_deposite_id=fix_deposite_id)

    if request.user.is_authenticated:
        profile = Account_holders.objects.get(username=request.user)
        name = profile.name
        email = profile.email
        mobile = profile.mobile
    else:
        name = None
        email = None
        mobile = None

    per_month = fix_deposit.fix_deposite_maximum_amt / fix_deposit.fix_deposite_month
    mataruity_amt = fix_deposit.fix_deposite_maximum_amt * fix_deposit.fix_deposite_rate_of_intrest * fix_deposit.fix_deposite_month

    context = {
        'name': name,
        'email': email,
        'mobile': mobile,
        'deposite_id': fix_deposit.fix_deposite_id,
        'deposite_name': fix_deposit.fix_deposite_name,
        'deposite_amount': fix_deposit.fix_deposite_maximum_amt,
        'rate': fix_deposit.fix_deposite_rate_of_intrest,
        'month': per_month,
        'month_word':fix_deposit.fix_deposite_month,
        'mataruity_amt': mataruity_amt,
        'mataruity_st_date': timezone.now().date(),
        'mataruity_end_date': (timezone.now() + timezone.timedelta(days=fix_deposit.fix_deposite_month * 30)).date(),
    }

    return render(request, 'service_dir/fix_deposite_details.html', context)


@login_required
def fix_deposite_process_payment(request):
    if request.method == 'POST':
        user = request.user
        profile = Account_holders.objects.get(username=user)
        bank_wallet = BankWallet.get_instance()

        fix_deposite_id = request.POST.get('fix_deposite_id', '')

        if not fix_deposite_id:
            return JsonResponse({'success': False, 'error': 'Fix deposit ID is missing'})

        # Debugging: Print out the values received in the POST request
        logger.debug("POST data: %s", request.POST)

        fix_deposite_amt = request.POST.get('fix_deposite_amt', '')
        fix_deposite_maturity_amt = request.POST.get('fix_deposite_maturity_amt', '')

        # Handle empty fields gracefully
        if not fix_deposite_amt or not fix_deposite_maturity_amt:
            return JsonResponse({'success': False, 'error': 'Amount fields are missing'})

        try:
            fix_deposite_amt = float(fix_deposite_amt)
            fix_deposite_maturity_amt = float(fix_deposite_maturity_amt)
        except ValueError:
            logger.error("Invalid value received for amount fields")
            return JsonResponse({'success': False, 'error': 'Invalid amount values'})

        transaction_slip(profile, 000, "Debited", "Fix Deposite", fix_deposite_id, fix_deposite_amt, "Credit Card","Complete")
        bank_wallet.bank_amount += float(fix_deposite_amt)
        bank_wallet.update_date = today_date()
        bank_wallet.save()


        fix_deposite_user = FixDepositeUsers(
            user=profile,
            username=profile.username,
            name=profile.name,
            email=profile.email,
            mobile=profile.mobile,
            fix_deposite_id=fix_deposite_id,
            fix_deposite_name=request.POST['fix_deposite_name'],
            fix_deposite_rate_of_intrest=float(request.POST['fix_deposite_rate_of_intrest']),
            fix_deposite_month=float(request.POST['fix_deposite_month']),
            fix_deposite_amt=fix_deposite_amt,
            fix_deposite_maturity_amt=fix_deposite_maturity_amt,
            fix_deposite_st_date=request.POST['fix_deposite_st_date'],
            fix_deposite_end_date=request.POST['fix_deposite_end_date'],
            fix_deposite_status='Running',
            fix_deposite_description=request.POST['fix_deposite_description'],
        )
        fix_deposite_user.save()
        inbox_message(profile, "Fix Deposite", "Fix Deposite is successfully Activated")

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def fix_deposite_payment_details(request):
    fixDeposite_id = request.GET.get('id')
    context = {}

    if not fixDeposite_id:
        messages.error(request, "Invalid fixed deposit ID.")
        return redirect('user_activity')  # Redirect to an appropriate page

    try:
        fixDeposite_user = FixDepositeUsers.objects.get(id=fixDeposite_id, username=request.user)

        if fixDeposite_user.fix_deposite_amt < fixDeposite_user.fix_deposite_paid_amt:
            messages.error(request, "Invalid Amount.")
            return redirect('user_activity')
        
        remain = fixDeposite_user.fix_deposite_amt - fixDeposite_user.fix_deposite_paid_amt

        context = {
            'fix_deposite_id': fixDeposite_user.id,
            'name': fixDeposite_user.name,
            'fix_deposite_amt': fixDeposite_user.fix_deposite_amt,
            'fix_deposite_rate_of_intrest': fixDeposite_user.fix_deposite_rate_of_intrest,
            'fix_deposite_month': fixDeposite_user.fix_deposite_month,
            'fix_deposite_st_date': fixDeposite_user.fix_deposite_st_date,
            'fix_deposite_end_date': fixDeposite_user.fix_deposite_end_date,
            'fix_deposite_maturity_amt': fixDeposite_user.fix_deposite_maturity_amt,
            'fix_deposite_paid_amt': fixDeposite_user.fix_deposite_paid_amt,
            'fix_deposite_status': fixDeposite_user.fix_deposite_status,
            'remaining': remain
        }
    except FixDepositeUsers.DoesNotExist:
        messages.error(request, "You do not have permission to view this fixed deposit.")
        return redirect('user_activity')  # Redirect to an appropriate page

    return render(request, 'service_dir/fix_deposit_payment.html', context)


@login_required
def fix_deposite_payment_process(request):
    if request.method == 'POST':
        user = request.user
        fix_deposite_id = request.POST.get('id')
        paid_amt = request.POST.get('pay_amt')

        profile = Account_holders.objects.get(username=user)
        bank_wallet = BankWallet.get_instance()


        if not fix_deposite_id:
            return JsonResponse({'success': False, 'error': 'Fix deposit ID is missing'})

        # Debugging: Print out the values received in the POST request
        logger.debug("POST data: %s", request.POST)

        try:
            fix_deposite_paid_amt = float(paid_amt)
        except ValueError:
            logger.error("Invalid value received for amount fields")
            return JsonResponse({'success': False, 'error': 'Invalid amount values'})

        transaction_slip(profile, 000, "Debited", "Fix Deposite", fix_deposite_id, paid_amt, "Credit Card","Complete")
        bank_wallet.bank_amount += float(paid_amt)
        bank_wallet.update_date = today_date()
        bank_wallet.save()

        fix_deposite = get_object_or_404(FixDepositeUsers, id=fix_deposite_id, username=request.user)
        fix_deposite.fix_deposite_paid_amt += float(paid_amt)
        fix_deposite.save()


        inbox_message(profile, "Fix Deposite", "Fix Deposite Amount paid")


        return redirect('activity')  # Redirect to an appropriate page

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


# ------------------------End Fix Deposite Data ------------------------------------


# ------------------------Customer Account List ------------------------------------
def customer_account_list(request):
    profile_holder = get_object_or_404(Account_holders, user=request.user)
    #customer_accounts = CustomerListAccountModel.objects.all()  # Fetch all customer accounts
    customer_accounts = CustomerListAccountModel.objects.filter(email=profile_holder.email)
    context = {
        'name': profile_holder.name,
        'customer_accounts': customer_accounts  # Pass customer accounts to the template
    }
    return render(request, 'user_setting_dir/customer_account_list.html', context)

def verify_account(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        account_no = data.get('account_no', None)
        if account_no is not None:
            try:
                account = Account_Details.objects.get(account_no=account_no)
                data = {
                    'exists': True,
                    'name': account.name,
                    'account_no': account.account_no,
                    'mobile_no': account.mobile,
                    'email_id': account.email
                }
            except Account_Details.DoesNotExist:
                data = {'exists': False}
            return JsonResponse(data)
    return JsonResponse({'error': 'Invalid request'})

def add_customer(request):
    if request.method == 'POST':
        profile_holder = get_object_or_404(Account_holders, user=request.user)
        data = json.loads(request.body)
        account_no = data.get('account_no', None)
        name = data.get('name', None)
        mobile_no = data.get('mobile_no', None)
        email_id = data.get('email_id', None)

        if account_no is not None and name is not None and mobile_no is not None and email_id is not None:
            try:
                account = Account_Details.objects.get(account_no=account_no)
                # Assuming CustomerAccount is your model for storing customer details
                print("hello")
                print(account.mobile)
                customer = CustomerListAccountModel.objects.create(
                    user=account,
                    username=profile_holder.username,
                    name=profile_holder.name,
                    email=profile_holder.email,
                    customer_username=account.username,
                    customer_account_no=account.account_no,
                    customer_name=account.name,
                    customer_mobile_no=account.mobile,
                    customer_email=account.email
                )
                inbox_message(profile_holder, "Add Customer", f"{account.name} had successfully added to the list.")
                return JsonResponse({'success': True})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
        else:
            return JsonResponse({'success': False, 'error': 'Missing required fields'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

@csrf_exempt
def delete_customer(request, account_no):
    if request.method == "DELETE":
        try:
            profile_holder = get_object_or_404(Account_holders, user=request.user)
            customer = CustomerListAccountModel.objects.get(customer_account_no=account_no)
            customer.delete()
            inbox_message(profile_holder, "Delete Custoter",f"{customer.name} had deleted from the list.")
            return JsonResponse({"success": True})
        except CustomerListAccountModel.DoesNotExist:
            return JsonResponse({"success": False, "error": "Customer not found"})
    return JsonResponse({"success": False, "error": "Invalid request method"})

def get_customer_accounts(request):
    if request.method == 'GET':
        profile_holder = get_object_or_404(Account_holders, user=request.user)
        accounts = CustomerListAccountModel.objects.filter(email=profile_holder.email).values('customer_account_no', 'customer_name', 'customer_email', 'customer_mobile_no')
        #accounts = CustomerListAccountModel.objects.all().values('customer_account_no', 'customer_name', 'customer_email', 'customer_mobile_no')
        accounts_list = list(accounts)
        return JsonResponse(accounts_list, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

# ------------------------End Customer Account List ------------------------------------

# ------------------------Transaction ------------------------------------
def fetch_transaction_months(request):
    profile_holder = get_object_or_404(Account_holders, user=request.user)
    transactions = UserTransactionDetails.objects.filter(email=profile_holder.email).values('transaction_date').annotate(count=Count('transaction_date'))
    months = {transaction['transaction_date'].strftime('%Y-%m') for transaction in transactions}

    return JsonResponse({'months': sorted(months)})

@csrf_exempt
def delete_transactions(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        months = data.get('months', [])

        if not months:
            return JsonResponse({'success': False, 'error': 'No months selected'}, status=400)

        try:
            for month in months:
                UserTransactionDetails.objects.filter(transaction_date__startswith=month).delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
def user_transaction_statement(request):
    profile_holder = get_object_or_404(Account_holders, user=request.user)
    transactions = UserTransactionDetails.objects.filter(username=request.user).order_by('-id')

    # Filtering
    # Filtering
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    transaction_type_filter = request.GET.get('transaction_type')
    status_filter = request.GET.get('status')
    sort_order = request.GET.get('sort_order')

    if start_date and end_date:
        transactions = transactions.filter(date__range=[start_date, end_date])
    if transaction_type_filter:
        transactions = transactions.filter(transaction_type=transaction_type_filter)
    if status_filter:
        transactions = transactions.filter(status=status_filter)
    if sort_order:
        transactions = transactions.order_by(sort_order)


    paginator = Paginator(transactions, 12)  # Show 30 transactions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'name':profile_holder.name,
        'page_obj': page_obj,
        'start_date': start_date,
        'end_date': end_date,
        'transaction_type_filter': transaction_type_filter,
        'status_filter': status_filter,
        'sort_order': sort_order
    }
    return render(request, 'users_dir/user_transaction_statement.html',context)

@login_required
def delete_transaction(request, id):
    transaction = UserTransactionDetails.objects.get(id=id, username=request.user)
    transaction.delete()
    return redirect('transaction_statement')

@login_required
def get_transactions(request):
    transactions = UserTransactionDetails.objects.filter(username=request.user)
    transaction_list = list(transactions.values(
        'loan_id',
        'amount',
        'transaction_type',
        'transaction_id',
        'payment_status',
        'payment_method',
        'transaction_date'
    ))
    return JsonResponse({'data': transaction_list})

# ------------------------End Transaction ------------------------------------

def get_account_email(request):
    if request.method == 'GET':
        account_holder = Account_holders.objects.get(user=request.user)
        return JsonResponse({'email': account_holder.email})
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def send_mail_view(request):
    if request.method == 'POST':
        account_holder = Account_holders.objects.get(user=request.user)
        data = json.loads(request.body)
        email = data.get('email')
        if email:
            try:
                # Fetch transaction data for the logged-in user
                transactions = UserTransactionDetails.objects.filter(email=account_holder.email)
                # Prepare data for the PDF table
                table_data = [['Transaction ID', 'Transaction Date', 'Type', 'Credited By', 'Amount', 'Payment Method',
                               'Payment Status', 'Description']]
                for transaction in transactions:
                    # Format the transaction date
                    formatted_date = format(transaction.transaction_date, 'M d, Y h:i A')
                    table_data.append(
                        [transaction.transaction_id, formatted_date, transaction.transaction_type, transaction.section,
                         transaction.amount, transaction.payment_method, transaction.payment_status,
                         transaction.description])

                pdf_file = generate_pdf(table_data)
                send_table_in_email(email, pdf_file)
                return JsonResponse({'message': 'Mail sent successfully'})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Email not provided'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def generate_pdf(table_data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    table = Table(table_data)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table.setStyle(style)
    elements = [table]
    doc.build(elements)
    buffer.seek(0)
    return buffer


def send_table_in_email(email, pdf_file):
    subject = 'Your Transaction Statement Of Mini Bank'
    message = 'Please download attached your transaction statement.'
    email_message = EmailMessage(subject, message, 'anshumk123@gmail.com', [email])
    email_message.attach('transaction_statement.pdf', pdf_file.read(), 'application/pdf')
    email_message.send()



@csrf_exempt
@login_required
def user_profile(request):
    if request.method == 'GET':
        profile_holder = get_object_or_404(Account_holders, user=request.user)
        account_details = get_object_or_404(Account_Details, username=profile_holder.username)
        card_details = ATMCardModel.objects.get(account_no=account_details.account_no)
        transactions_by_otp = TransactionSetByOtp.objects.filter(user=account_details).order_by('-issue_date')

        formatted_date_time_str = today_date_time()
        kolkata_time = datetime.strptime(formatted_date_time_str, '%Y-%m-%d %I:%M %p')
        expiration_time = kolkata_time + timedelta(minutes=15)
        expiration_time_iso = expiration_time.isoformat()

        context = {
            'name': profile_holder.name,
            'account_details': account_details,
            'profile_holder': profile_holder,
            'card_details': card_details,
            'net_banking_service': card_details.net_banking_service,
            'withdraw_service': card_details.withdraw_service,
            'atm_card_status': card_details.atm_card_status,
            'money_transfer_service': card_details.money_transfer_service,
            'transactions_by_otp':transactions_by_otp,
            'expiration_time_iso':expiration_time_iso,
            'image_path':profile_holder.profile_photo if profile_holder.profile_photo else ""
        }

        return render(request, 'users_dir/user_profile.html',context)


# -------------------------------Action Center-------------------------------

def action_center(request):
    profile_holder = get_object_or_404(Account_holders, user=request.user)
    actions = ActionCenterModel.objects.filter(username=profile_holder.username)
    context ={
        'name':profile_holder.name,
        'actions': actions
    }
    return render(request, 'users_dir/action_center.html',context)

def action_detail(request, id):
    action = ActionCenterModel.objects.get(id=id)
    data = {
        'subject': action.subject,
        'content': action.content,
    }
    return JsonResponse(data)
# ------------------------------- End Action Center-------------------------------



# ------------------------------- ATM view-------------------------------
def atm_card_view(request):
    profile_holder = get_object_or_404(Account_holders, user=request.user)
    account_details = get_object_or_404(Account_Details, username=profile_holder.username)
    card_details = ATMCardModel.objects.get(account_no=account_details.account_no)
    chunks = [card_details.card_number[i:i + 4] for i in range(0, len(card_details.card_number), 4)]

    context = {
        'card_details':card_details,
        'chunks':chunks
    }
    return render(request, 'users_dir/atm_card_view.html',context)

@csrf_exempt
def update_service(request):
    if request.method == 'POST':
        service_type = request.POST.get('service_type')
        enable = request.POST.get('enable') == 'true'
        account_no = request.POST.get('account_no')

        try:
            card_details = ATMCardModel.objects.get(account_no=account_no)
            enable_value = 1 if enable else 0

            if service_type == 'atm_card_status':
                card_details.atm_card_status = enable_value
                if not enable:
                    card_details.money_transfer_service = 0
                    card_details.withdraw_service = 0
                    card_details.net_banking_service = 0
            elif service_type == 'money_transfer_service' and card_details.atm_card_status:
                card_details.money_transfer_service = enable_value
            elif service_type == 'withdraw_service' and card_details.atm_card_status:
                card_details.withdraw_service = enable_value
            elif service_type == 'net_banking_service' and card_details.atm_card_status:
                card_details.net_banking_service = enable_value

            card_details.save()
            return JsonResponse({
                'status': 'success',
                'atm_card_status': card_details.atm_card_status,
                'money_transfer_service': card_details.money_transfer_service,
                'withdraw_service': card_details.withdraw_service,
                'net_banking_service': card_details.net_banking_service,
            })
        except ATMCardModel.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Account not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def ATMTransactionView(request):

    if request.method == 'GET':

        atm_card_number = request.GET.get('atm_card_number')
        amount = request.GET.get('amount')
        pin = request.GET.get('pin')
        otp = request.GET.get('otp')
        account_no = request.GET.get('account_no')

        response = {}
        request_otp={}
        try:
            card_details = ATMCardModel.objects.get(card_number=atm_card_number)
        except ATMCardModel.DoesNotExist:
            response['message'] = 'Invalid ATM Crad Number'
            return JsonResponse(response)


        # Check if the ATM card number is provided
        if not atm_card_number:
            response['success'] = False
            response['message'] = 'ATM card number is required'
            return JsonResponse(response)

        # Get the ATM card
        atm_card = get_object_or_404(ATMCardModel, card_number=atm_card_number)
        account_holder = get_object_or_404(Account_holders, username=atm_card.username)

        # Check PIN
        if pin and not atm_card.pin == pin:
            response['success'] = False
            response['message'] = 'Invalid PIN'
            return JsonResponse(response)

        # Check OTP
        if otp:
            try:
                otp_record = TransactionSetByOtp.objects.get(atm_card_number=atm_card_number, otp=otp)
                if otp_record.transaction_status == 0 and otp_record.transaction_action == 0:
                    response['success'] = False
                    response['message'] = 'OTP Expired'
                    return JsonResponse(response)

                request_otp=otp_record
            except TransactionSetByOtp.DoesNotExist:
                response['success'] = False
                response['message'] = 'Invalid OTP'
                return JsonResponse(response)

        # Handle different types of transactions
        if atm_card.atm_card_status:

            if request_otp:
                if atm_card.withdraw_service:
                    account_details = get_object_or_404(Account_Details, account_no=request_otp.account_no)
                    user_current_amt = account_details.current_amt
                    otp_request_amount = otp_record.amount

                    if user_current_amt<otp_request_amount:
                        response['message'] = 'Insufficient Balance'
                        return JsonResponse(response)

                    account_details.current_amt -= otp_request_amount
                    account_details.save()

                    otp_record = TransactionSetByOtp.objects.get(atm_card_number=atm_card_number, otp=otp)
                    otp_record.transaction_status = 0
                    otp_record.transaction_action = 0
                    otp_record.save()

                    transaction_slip(account_holder, 000, "Debited", "Withdraw", "Withdraw by OTP", otp_request_amount, "ATM Machine","Complete")
                    inbox_message(account_holder, "ATM Usages",f"Money Rs. {otp_request_amount} Successfully Debited to your account \n Now you OTP {otp} is Expired.\n Thank you for using otp withdraw process.")

                    response['success'] = True
                    response['balance'] = otp_request_amount
                    response['message'] = 'Transaction By OTP successful done'
                    return JsonResponse(response)
                else:
                    response['success'] = False
                    response['message'] = 'ATM card withdraw services are not activated'


            elif amount and not account_no:
                if atm_card.withdraw_service:
                    account_details = get_object_or_404(Account_Details, account_no=atm_card.account_no)
                    user_current_amt = account_details.current_amt
                    requested_amount = float(amount)

                    if requested_amount > user_current_amt:
                        response['success'] = False
                        response['message'] = 'Insufficient funds'
                        return JsonResponse(response)
                    else:
                        account_details.current_amt -= requested_amount
                        account_details.save()

                        transaction_slip(account_holder, 000, "Debited", "Withdraw", "withdraw cash", requested_amount,"ATM Machine", "Complete")
                        inbox_message(account_holder, "ATM Usages",f"Money Rs. {requested_amount} Successfully Debited to your account \n \n Thank you for using MINI Bank.")

                        response['success'] = True
                        response['balance'] = requested_amount
                        response['message'] = 'Withdraw Money'
                        return JsonResponse(response)
                else:
                    response['success'] = False
                    response['message'] = 'ATM card withdraw services are not activated'

            elif account_no and amount :
                if atm_card.money_transfer_service:

                    try:
                        account = Account_Details.objects.get(account_no=account_no)
                    except Account_Details.DoesNotExist:
                        response['success'] = False
                        response['message'] = 'Invalid account number'
                        return JsonResponse(response)

                    account_details = get_object_or_404(Account_Details, account_no=atm_card.account_no)
                    user_current_amt = account_details.current_amt
                    requested_transfer_amount = float(amount)

                    if requested_transfer_amount > user_current_amt:
                        response['success'] = False
                        response['message'] = 'Insufficient funds'
                        return JsonResponse(response)
                    else:
                        account_details.current_amt -= requested_transfer_amount
                        account.current_amt += requested_transfer_amount
                        account_details.save()
                        account.save()

                        transaction_slip(account_holder, 000, "Debited", "Transfer", "transfer", requested_transfer_amount,"ATM Machine", "Complete")
                        inbox_message(account_holder, "ATM Usages",f"Money Rs. {requested_transfer_amount} Successfully transfer to the {account.name} account. \n \n Thank you for using MINI Bank.")

                        response['success'] = True
                        response['balance'] = requested_transfer_amount
                        response['message'] = 'Transfer successful'
                        return JsonResponse(response)
                else:
                    response['success'] = False
                    response['message'] = 'ATM card transfer services are not activated'

            else:
                account_details = get_object_or_404(Account_Details, account_no=card_details.account_no)
                current_amt = account_details.current_amt
                response['success'] = True
                response['balance'] = current_amt
                return JsonResponse(response)
        else:
            response['success'] = False
            response['message'] = 'ATM card services are not activated'
            return JsonResponse(response)

    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)
# -------------------------------End ATM view----------------------------


# -------------------------------Transaction By OTP-----------------------
@csrf_exempt
def make_otp_transaction(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        amount = float(data.get('amount'))
        pin = data.get('pin')
        account_no = data.get('account_no')



        try:
            card_details = ATMCardModel.objects.get(account_no=account_no)
            account_details = Account_Details.objects.get(account_no=account_no)

            if card_details.pin == pin:
                formatted_date_time_str = today_date_time()
                kolkata_time = datetime.strptime(formatted_date_time_str, '%Y-%m-%d %I:%M %p')
                expire_date = kolkata_time + timedelta(minutes=10)
                date_obj = datetime.strptime(formatted_date_time_str, '%Y-%m-%d %I:%M %p')
                otp = generate_otp()

                expiration_time = kolkata_time + timedelta(minutes=15)
                expiration_time_iso = expiration_time.isoformat()

                transaction = TransactionSetByOtp.objects.create(
                    user=account_details,
                    username=card_details.username,
                    name=card_details.name,
                    email=card_details.email,
                    mobile=account_details.mobile,  # Assuming mobile is a field in Account_Details
                    transactionbyotp_id=generate_unique_transactionByOtp_id(),
                    otp=otp,  # You would generate and handle OTP appropriately
                    account_no=account_details.account_no,
                    amount=amount,
                    transaction_action=1,
                    atm_card_number=card_details.card_number,
                    transaction_status=False,
                    issue_date=date_obj,
                    expire_date=expiration_time_iso,
                    description='Transaction completed'
                )
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid PIN'})
        except ATMCardModel.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Account not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

@require_http_methods(["DELETE"])
def delete_transactionByOtp(request, transaction_id):
    try:
        transaction = TransactionSetByOtp.objects.get(transactionbyotp_id=transaction_id)
        transaction.delete()
        return JsonResponse({'status': 'success'}, status=200)
    except TransactionSetByOtp.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Transaction not found'}, status=404)

@csrf_exempt
@require_POST
def transactionotp_end_session(request, transaction_id):
    if request.method == 'POST':
        print(transaction_id)  # Debugging line to verify transaction_id
        transaction = get_object_or_404(TransactionSetByOtp, transactionbyotp_id=transaction_id)

        transaction.transaction_status = False
        transaction.transaction_action = False
        transaction.save()

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'fail'})


# -------------------------------End Transaction By OTP-----------------------


@csrf_exempt
def save_photo(request):
    if request.method == 'POST':
        try:
            base64_image = request.POST.get('base64_image')
            if base64_image:
                filename = request.user.username
                file_path = convert_base64_to_image(base64_image, filename)
                code = convert_image_to_base64(file_path)

                profile_holder = get_object_or_404(Account_holders, user=request.user)
                profile_holder.profile_photo = file_path
                profile_holder.photo = code
                profile_holder.save()

                new_image_url = f"{settings.MEDIA_URL}{file_path}".replace('\\', '/')
                print(new_image_url)
                return JsonResponse({'success': True, 'new_image_url': new_image_url})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def remove_photo(request):
    if request.method == 'POST':
        try:
            profile_holder = get_object_or_404(Account_holders, user=request.user)
            profile_holder.profile_photo = None
            profile_holder.photo = ""
            profile_holder.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
