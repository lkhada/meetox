from statistics import mode
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AppUser(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    role = models.CharField(max_length=10)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    notes = models.TextField(null=True)
    app_user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='slots')
