# feedback/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('employee/<str:eid>/feedback/', views.feedback, name='feedback'),
]
