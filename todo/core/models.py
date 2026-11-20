from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    title = models.CharField(max_length=50)
    created_at = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)
    