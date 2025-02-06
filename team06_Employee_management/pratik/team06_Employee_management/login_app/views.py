from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.models import User
from .forms import RegistrationForm, LoginForm, greeting_fun
from django.contrib import messages
import datetime
from django.forms import modelform_factory
from .models import Admin_data
 
import MySQLdb
 
try:
    # Establish the database connection
    db = MySQLdb.connect(
        host="localhost",
        user="root",
        db="system_development_t06"
    )
   
    # Create a cursor object to interact with the database
    print("Database connection successful")
except:
    print("Error: Database connection failed")
 
 
 
 
 
def index(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
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
            cursor = db.cursor()
            print(user)
            cursor.execute("""INSERT INTO `employee_details` (`Employee_Name`, `EID`,
                           `Employee_Number`, `Email`, `Date_of_Birth`, `Role`,
                           `Management_Level`, `Home_Office`, `Team_ID`, `Position`,
                           `PL_ID`, `Manager_ID`, `Profile_Image`)
                           VALUES (NULL, %s, NULL,
                           NULL, NULL,
                           NULL, NULL, NULL, %s, NULL, %s, %s, NULL);""", [user,'T00','chris.wang','chris.wang'])
            db.commit()
           
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
 
# def admin_login(request):
#     AdminForm = modelform_factory(Admin_data, exclude = [])
#     if request.method == 'POST':
#         form = AdminForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = admin_authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 messages.success(request, 'Login successful!')
#                 return redirect('welcome')
#             else:
#                 messages.error(request, 'Invalid login credentials.')
#     else:
#         form = AdminForm()
#     return render(request, 'admin_login.html', {'form': form})
 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
 
class AdminForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
 
def create_admin_user(username, password):
    if User.objects.filter(username=username).exists():
        print('Admin user with this username already exists.')
    else:
        user = User.objects.create_user(username=username, password=password)
        user.is_staff = True  # Mark user as staff/admin
        user.save()
        print(f'Admin user "{username}" created successfully.')
 
# Example usage
create_admin_user('myadmin', 'pass@123')
 
def admin_login(request):
    if request.method == 'POST':
        form = AdminForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('welcome')  # Ensure 'welcome' view exists
            else:
                messages.error(request, 'Invalid login credentials.')
    else:
        form = AdminForm()
    return render(request, 'admin_login.html', {'form': form})
 
def welcome(request):
    greeting = greeting_fun()
    user = request.user
    print(user, 'yes')
    if request.user.is_authenticated:
        user = request.user
    
        try:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM `employee_details` WHERE EID = %s;", [str(user)])
 
            userdata = cursor.fetchall()[0]
            employee_id = userdata[1]
            name = userdata[0]
            role = userdata[5]
            email = userdata[3]
            location = userdata[7]
            level = userdata[6]
            image = userdata[12]
            print(image,'yes')
 
 
 
            cursor.execute("SELECT * FROM `team_details` WHERE team_id = %s;", [str(userdata[8])])
            team = cursor.fetchall()[0]
            teamname = team[1]
 
            cursor.execute("""SELECT t1.EID as eid, t2.manager_id, t2.manager_name, t4.project_name,t3.pl_id,t3.pl_name,t5.project_name
                                FROM `employee_details` as t1
                                INNER JOIN
                                manager_details as t2
                                ON t1.Manager_ID = t2.manager_id
                                INNER JOIN
                                people_lead_details as t3
                                ON t1.PL_ID = t3.pl_id
                                INNER JOIN
                                team_details as t4
                                ON t2.team_id = t4.team_id
                                INNER JOIN
                                team_details as t5
                                ON t3.team_id = t5.team_id
                                WHERE eid = %s;""", [str(user)])
            add_info = cursor.fetchall()[0]
            manager_id = add_info[1]
            manager_name = add_info[2]
            man_project_name = add_info[3]
            pl_id = add_info[4]
            pl_name = add_info[5]
            pl_project_name = add_info[6]
 
 
 
        except:
            messages.error(request, 'User Data Found')
        username = ' '.join(str(user).split('.')).title()
        is_admin = False
        if user.username == 'myadmin':
            is_admin = True
        return render(request, 'welcome.html', {'username': username,
                                                'user': user,
                                                'employee_id' : employee_id ,
                                                'name': name,
                                                'role': role,
                                                'email': email,
                                                'location': location,
                                                'level': level,
                                                'teamname': teamname,
                                                'manager_id': manager_id,
                                                'image': image,
                                                'manager_name': manager_name,
                                                'man_project_name':man_project_name,
                                                'pl_id': pl_id,
                                                'pl_name': pl_name,
                                                'pl_project_name': pl_project_name,
                                                'greeting': greeting,
                                                'is_admin':is_admin})
   
    else:
        messages.error(request, 'You must be logged in to view this page.')
        return redirect('index')
    return render(request, 'welcome.html')
 
 
def help(request):
    return render(request, 'help.html')
 
def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')