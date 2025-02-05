from django import forms
from django.contrib.auth.forms import UserCreationForm
from admin_search.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['employee_name', 'employee_number', 'email', 
                  'date_of_birth', 'role', 'management_level', 
                  'home_office', 'team_id', 'position', 'pl_id', 
                  'manager_id', 'profile_image']