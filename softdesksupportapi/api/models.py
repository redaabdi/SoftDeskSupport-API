from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
 
class User(AbstractUser):
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    age = models.IntegerField(blank=False)

class Project(models.Model) :
    class Type(models.TextChoices):
        BACK_END = "back-end"
        FRONT_END = "front-end"
        IOS = "ios"
        ANDROID = "android"
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="project_set_author")
    type = models.CharField(max_length=10, choices=Type.choices, blank=True)

class Contributor(models.Model) :
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    class Meta:
        unique_together = ("user", "project")
