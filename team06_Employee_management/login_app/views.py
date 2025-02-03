from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.models import User
from .forms import RegistrationForm, LoginForm
from django.contrib import messages
import datetime
from django.forms import modelform_factory
from .models import Admin_data

def index(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('welcome')
            else:
                messages.error(request, 'Invalid login credentials.')
    else:
        form = LoginForm()
    return render(request, 'index.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('index')
        else:
            messages.error(request, 'Registration failed. Please try again.')
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})

def admin_authenticate(request, username=None, password=None):
        try:
            user = Admin_data.objects.get(username=username)
            if user.check_password(password):
                return user
        except Admin_data.DoesNotExist:
            return None

def admin_login(request):
    AdminForm = modelform_factory(Admin_data, exclude = [])
    if request.method == 'POST':
        form = AdminForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = admin_authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('welcome')
            else:
                messages.error(request, 'Invalid login credentials.')
    else:
        form = AdminForm()
    return render(request, 'admin_login.html', {'form': form})

def welcome(request):
    user = request.user
    if request.user.is_authenticated:
        user = request.user
        return render(request, 'welcome.html', {'user': user})
    
    else:
        messages.error(request, 'You must be logged in to view this page.')
        return redirect('index')
    return render(request, 'welcome.html')















def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')