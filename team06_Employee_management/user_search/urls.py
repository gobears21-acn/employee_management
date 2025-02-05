from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_search, name='user_search'),
    path('welcome/', views.welcome, name='welcome'),
    path('team/', views.team, name='team'),
]