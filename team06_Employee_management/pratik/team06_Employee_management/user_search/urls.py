from django.urls import path
from . import views

urlpatterns = [
    path('user_search/', views.user_search, name='user_search'),
    path('welcome/', views.welcome, name='welcome'),
    path('team/', views.team, name='team'),
    path('employee/<str:id>/', views.employee_detail, name='employee_detail'),
]