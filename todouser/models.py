from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class Todoapp(models.Model): 

    tname = models.CharField(max_length=200)
    desc = models.TextField()
    status=models.CharField(max_length=100)
    priority=models.CharField(max_length=100)
    completion_date=models.DateField(blank=True, null=True)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


    def days_remaining(self):
        if self.completion_date == timezone.now().date():
            return ("Last day of task completion!")
        elif self.completion_date > timezone.now().date():
            if self.completion_date:
                today = timezone.now().date()        
                remaining_days = (self.completion_date - today).days
                return (f"{remaining_days} Dyas left!")
        return ("Task completion date ended!")