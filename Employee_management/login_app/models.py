from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Admin_data(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)