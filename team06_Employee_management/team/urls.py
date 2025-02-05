from django.urls import path
from django.urls import path
from .views import team_page

urlpatterns = [
    path('team/<int:team_id>/', team_page, name='team_page'),
]