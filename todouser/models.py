from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Todoapp(models.Model):
    tname = models.CharField(max_length=50)
    desc = models.TextField()
    status=models.CharField(max_length=50)
    priority=models.CharField(max_length=50)
    completion_date=models.DateField(blank=True, null=True)
    remaining_days = models.CharField(max_length=50)
    created_at=models.DateTimeField(default=timezone.now)
    updated_at=models.DateTimeField(default=timezone.now)
    newuser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="newuser")
    
    def _str__(self):
        return self.tname

    def get_absolute_url(self):
        return reverse("todo-detail", kwargs={"pk": self.pk})
    