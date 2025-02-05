from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_search, name='admin_search'),
    path('delete/<int:pk>/', views.delete_user, name='delete_user'),
    path('add/', views.add_user, name='add_user'),
]