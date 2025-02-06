# employee/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('training-history/', views.employee_training_history, name='employee_training_history'),
]
