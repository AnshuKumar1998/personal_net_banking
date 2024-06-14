import random
from datetime import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from app.models import Contact_us,Account_holders,Account_Details,User_Inbox
from app.forms import UserForm
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt


def master(request):
    return render(request,'master.html')


def index(request):
    return render(request,'index.html')

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
            try:
                profile = Account_holders.objects.get(user=user)
                user_messages = User_Inbox.objects.filter(username=profile.username)
                try:
                    account_data = Account_Details.objects.get(username=username)
                except Account_Details.DoesNotExist:
                    account_data = None  # Handle case where account details don't exist

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
                    'messages': user_messages  # Ensure messages are included in the context
                }
            except Account_holders.DoesNotExist:
                profile_data = {}
                messages.error(request, 'User account does not exist.')  # Handle if user account does not exist
            except Exception as e:
                profile_data = {}
                messages.error(request, f'Error: {str(e)}')  # Handle other exceptions

            context = {
                'profile_data': profile_data,
            }

            return render(request, 'users_dir/user_account.html', context)
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'users_dir/login.html')

@login_required
def user_account(request):
    try:
        profile = Account_holders.objects.get(user=request.user)
        try:
            account_data = Account_Details.objects.get(username=profile.username)
        except Account_Details.DoesNotExist:
            account_data = None

        user_messages = User_Inbox.objects.filter(username=profile.username)

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
    response = redirect('login')  # Redirect to the login page or any other page after logout
    response.delete_cookie('sessionid')  # Delete the session cookie
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

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Error: This email is already registered.')
        elif Account_holders.objects.filter(mobile=mobile).exists():
            messages.error(request, 'Error: This mobile number is already registered.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Error: This username is already registered.')
        else:
            user = User(username=username, email=email, password=make_password(password))
            user.save()
            profile = Account_holders.objects.create(user=user, username=username, name=name,email=email, gender=gender, mobile=mobile, dob=dob, password=password, address=address)
            profile.save()
            User_Inbox.objects.create(
                user=profile,
                username=username,
                name=name,
                email=email,
                mobile=mobile,
                subject="Welcome to Our Service",
                content="Thank you for creating an account with us.",
                date=timezone.now().date()
            )
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
            name=account_holder.mobile,
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
        User_Inbox.objects.create(
            user=account_holder,
            username=account_holder.username,
            name=account_holder.name,
            email=account_holder.email,
            mobile=account_holder.mobile,
            subject="Account Activation",
            content="Your account has been successfully activated.",
            date=timezone.now().date()
        )

        messages.success(request, 'Account Successfully Activated')#
        return redirect('user_account')

    return render(request, 'users_dir/user_account.html')


def generate_unique_account_number():
    while True:
        # Generate random 8-digit number
        account_number = random.randint(10000000, 99999999)  # Random number between 10000000 and 99999999

        # Check if account number already exists in database
        if not Account_Details.objects.filter(account_no=account_number).exists():
            return account_number

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
        User_Inbox.objects.create(
            user=account_holder,
            username=account_holder.username,
            name=account_holder.name,
            email=account_holder.email,
            mobile=account_holder.mobile,
            subject="Profile Update",
            content="Your profile has been successfully Updated.",
            date=timezone.now().date()
        )
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