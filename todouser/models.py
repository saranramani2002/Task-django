from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Todoapp(models.Model):

    # STATUS_CHOICES = [
    #     ("Completed", "Completed"),
    #     ("In-progress", "In-progress"),
    #     ("Not-completed", "Not-completed"),
    # ]

    # PRIORITY_CHOICES =[
    #     ("Low","Low"),
    #     ("Medium", "Medium"),
    #     ("High", "High"),
    # ]

    
    # def remaining_days(self):
    #     if self.completion_date:
    #         today = date.today()
    #         remaining = self.completion_date - today
    #         return remaining.days
    #     else:
    #         None
    
    def days_remaining(self):
        if self.completion_date:
            today = date.today()
            remaining_days = (self.completion_date - today).days
            return max(0, remaining_days)
        return None 

    tname = models.CharField(max_length=200)
    desc = models.TextField()
    status=models.CharField(max_length=100)
    priority=models.CharField(max_length=100)
    completion_date=models.DateField()
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def _str__(self):
        return self.tname
