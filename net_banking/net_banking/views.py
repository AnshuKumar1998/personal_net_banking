from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from app.models import Contact_us,Account_holders
from app.forms import UserForm



def master(request):
    return render(request,'master.html')


def index(request):
    return render(request,'index.html')


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
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_account')
        else:
            messages.error(request, "Invalid username or password.")
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

        if Account_holders.objects.filter(email=email).exists():
            messages.error(request, 'Error: This email is already registered.')
        elif Account_holders.objects.filter(mobile=mobile).exists():
            messages.error(request, 'Error: This mobile number is already registered.')
        elif Account_holders.objects.filter(username=username).exists():
            messages.error(request, 'Error: This username is already registered.')
        else:
            user = Account_holders(username=username, name=name, gender=gender, email=email, mobile=mobile, dob=dob, address=address, password=password)
            user.save()
            messages.success(request, 'Your Account Has Been Created successfully!')
            return redirect('signup')

    return render(request, 'users_dir/signup.html')