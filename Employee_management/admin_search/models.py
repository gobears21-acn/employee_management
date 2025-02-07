from django.db import models

class CustomUser(models.Model):
    employee_name = models.CharField(max_length=100)
    employee_number = models.CharField(max_length=100)
    email = models.EmailField()
    date_of_birth = models.DateField()
    role = models.CharField(max_length=100)
    management_level = models.CharField(max_length=100)
    home_office = models.CharField(max_length=100)
    team_id = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    pl_id = models.CharField(max_length=100)
    manager_id = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.employee_name