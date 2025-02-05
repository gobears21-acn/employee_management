from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    email = models.EmailField()
    is_leader = models.BooleanField(default=False)