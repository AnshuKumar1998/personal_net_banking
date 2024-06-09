from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from app.models import Contact_us


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