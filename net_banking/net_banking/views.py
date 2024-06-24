import uuid
import json
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from datetime import datetime
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.db.models import F, ExpressionWrapper, FloatField, Q
from django.http import JsonResponse, HttpResponse
from app.models import Contact_us,Account_holders,Account_Details,User_Inbox,MonthlyProfit,UserLoanDetails,UserTransactionDetails,BankWallet,FixDepositeList,FixDepositeUsers,Post,AdminMessage,Complaint
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from app.help import today_date, generate_unique_loan_id, calculate_due_date, generate_unique_account_number, inbox_message,transaction_slip
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import logging
from django.core.paginator import Paginator

logger = logging.getLogger(__name__)



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
    return render(request,'contact_us.html')



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
    response.delete_cookie('sessionid')  # Delete the session cookie
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


def get_profit_data(request):
    data = MonthlyProfit.objects.all().values('month', 'profit')
    return JsonResponse(list(data), safe=False)

@login_required
def chart_view(request):
    return render(request, 'users_dir/blog.html')

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
# -------------------------------End Loan Related Function-----------------------
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


def service(request):
    return render(request, 'service_dir/service.html')


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
            fix_deposite_status='Processing',
            fix_deposite_description=request.POST['fix_deposite_description'],
        )
        fix_deposite_user.save()
        inbox_message(profile, "Fix Deposite", "Fix Deposite is successfully Activated")

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def post_list(request):
    posts = Post.objects.all().order_by('-date')
    paginator = Paginator(posts, 5)  # Show 5 posts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'post_list.html', {'page_obj': page_obj})

@csrf_exempt
def like_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        post.likes += 1
        post.save()
        return JsonResponse({'likes': post.likes})


@login_required
def user_setting(request):
    return render(request,'user_setting_dir/user_setting.html')

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
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
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

        messages.success(request, 'Your complaint has been successfully sent!')
        return redirect(reverse('complaint_form'))

    recent_complaints = Complaint.objects.all().order_by('-created_at')[:5]
    return render(request, 'user_complaint.html', {'recent_complaints': recent_complaints})


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
            account_holder = Account_holders.objects.get(username=request.user.username)
            user_name = account_holder.name

            # Example: Perform money transfer logic here
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
                    return JsonResponse({'message': 'Recipient account not found.'}, status=404)

            else:
                #messages.error(request, 'Insufficient balance to transfer money.')
                return JsonResponse({'message': 'Insufficient balance to transfer money.'}, status=400)

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

