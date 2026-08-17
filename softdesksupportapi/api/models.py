from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
 
class User(AbstractUser):
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    age = models.IntegerField(blank=False)

class Project(models.Model) :
    name = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=1000, blank=True)
    contributors = models.ManyToManyField(settings.AUTH_USER_MODEL)
