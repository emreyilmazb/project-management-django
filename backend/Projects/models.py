from django.db import models
from django.conf import settings
from users.models import CustomUser

class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length = 200, default="Description")
    start_date = models.DateField(default='2024-10-18')
    end_date = models.DateField(default='2024-10-18')
    project_manager = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='projects')
    team_members = models.ManyToManyField(CustomUser, blank=True)
    
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['start_date']  # Sort projects by start date by default

class Task(models.Model):
    TASK_STATUSES = (
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=100)
    description = models.TextField()
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='tasks')
    status = models.CharField(max_length=20, choices=TASK_STATUSES, default='todo')
    def __str__(self):
        return self.title