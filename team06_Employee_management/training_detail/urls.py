# training_detail/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('training_history/', views.employee_training_history, name='training_history'),
]