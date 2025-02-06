from django.urls import path
from . import views

app_name = 'admin_search'

urlpatterns = [
    path('', views.admin_search, name='admin_search'),
    path('delete/<str:EID>/', views.delete_user, name='delete_user'),
    #path('add/', views.add_user, name='add_user'),
]