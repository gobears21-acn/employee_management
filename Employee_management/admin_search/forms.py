from django import forms
from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['employee_name', 'employee_number', 'email', 'date_of_birth', 
                  'role', 'management_level', 'home_office', 'team_id', 'position', 
                  'pl_id', 'manager_id', 'profile_image']