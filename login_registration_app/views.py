from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
import bcrypt

# Create your views here.

def homePage(request):
    return render(request, 'homePage.html')

def verify_registration(request):
    errors = User.objects.userValidation(request.POST)
    user_email = User.objects.filter(email = request.POST['email'])
    if user_email:
        messages.error(request, "Email already exists")
        return redirect('/')

    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect('/')

    password = request.POST['password']
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    new_user = User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = hashed_password
        )
    request.session['logged_in_user'] = new_user.id
    return redirect('/success')

def verify_login(request):
    user = User.objects.filter(email=request.POST['login_email'])
    if user:
        login_user = user[0]
        if bcrypt.checkpw(request.POST['login_password'].encode(), login_user.password.encode()):
            request.session['logged_in_user'] = login_user.id
            return redirect('/success')
        else:
            messages.error(request, "Invalid email or password")
            return redirect('/')
    messages.error(request, "Invalid email address")
    return redirect('/')

def login_successful(request):
    context = {
        "user": User.objects.get(id=request.session['logged_in_user'])
    }
    return render(request, 'success.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')