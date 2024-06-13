from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from app.models import Contact_us,Account_holders
from app.forms import UserForm



def master(request):
    return render(request,'master.html')


def index(request):
    return render(request,'index.html')

def rou(request):
    return render(request,'users_dir/rough.html')


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

        # More debugging
        if user is not None:
            auth_login(request, user)
           # return redirect('users_dir/user_account')
            return render(request, 'users_dir/user_account.html')
        else:
            return HttpResponse('Invalid username or password')

    return render(request, 'users_dir/login.html')


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
            messages.success(request, 'Your Account Has Been Created successfully!')
        return redirect('signup')

    return render(request, 'users_dir/signup.html')