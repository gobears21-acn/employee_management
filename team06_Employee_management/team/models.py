from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    employee_name = models.CharField(max_length=100)
    employee_number = models.CharField(max_length=100, unique=True)
    date_of_birth = models.DateField()
    role = models.CharField(max_length=100)
    management_level = models.CharField(max_length=100)
    home_office = models.CharField(max_length=100)
    team_identifier = models.CharField(max_length=100, default='default_team_id')  
    job_position = models.CharField(max_length=100)
    pl_identifier = models.CharField(max_length=100)
    manager_identifier = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='team_customuser_set',  
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='team_customuser_set',  
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def __str__(self):
        return self.username

class Team(models.Model):
    team_identifier = models.CharField(max_length=100, unique=True, default='default_team_id')
    team_name = models.CharField(max_length=100)

    def __str__(self):
        return self.team_name

class TeamMember(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    member_position = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.employee_name} - {self.member_position}"