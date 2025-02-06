from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    employee_name = models.CharField(max_length=100)
    employee_number = models.CharField(max_length=100, unique=True)
    date_of_birth = models.DateField()
    role = models.CharField(max_length=100)
    management_level = models.CharField(max_length=100)
    home_office = models.CharField(max_length=100)
    team_id = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    pl_id = models.CharField(max_length=100)
    manager_id = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_customuser_set',  # 修改related_name参数
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_customuser_set',  # 修改related_name参数
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def __str__(self):
        return self.username