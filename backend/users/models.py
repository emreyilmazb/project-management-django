from django.db import models
from django.contrib.auth.models import AbstractUser
            
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('team_lead', 'Team Leader'),
        ('intern', 'Intern Employee'),
    )
    user_type = models.CharField(max_length=100, choices=USER_TYPE_CHOICES, default='intern')
    def __str__(self):
        return self.username