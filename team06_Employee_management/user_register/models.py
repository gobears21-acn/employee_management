from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    member_count = models.IntegerField(default=0)

class Team(models.Model):
    name = models.CharField(max_length=100)
    project_name = models.CharField(max_length=100)
    lead_manager = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True, related_name='lead_manager')

class Employee(models.Model):
    user = models.OneToOneField('admin_search.CustomUser', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    employee_number = models.CharField(max_length=50, unique=True)
    date_of_birth = models.DateField()
    role = models.CharField(max_length=100)
    management_level = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    position = models.CharField(max_length=100)
    pl_id = models.CharField(max_length=50)
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField()
    office = models.CharField(max_length=100)