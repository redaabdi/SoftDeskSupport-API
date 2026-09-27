from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
import uuid

def get_or_create_anonymous_user():
    user = User.objects.get_or_create(
        username="anonymous_user",
        defaults={
            "can_be_contacted": False,
            "can_data_be_shared": False,
            "age": 15,
        }
    )
    user = user[0]
    return user

class User(AbstractUser):
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    age = models.IntegerField(blank=False)
    created_time = models.DateTimeField(auto_now_add=True)

class Project(models.Model) :
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True)
    type = models.CharField(
        max_length=10,
        choices = [
        ("back-end", "Back-end"),
        ("front-end", "Front-end"),
        ("ios", "iOS"),
        ("android", "Android")
        ],
        blank=True
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_or_create_anonymous_user), related_name="project_set_author")
    created_time = models.DateTimeField(auto_now_add=True)

class Contributor(models.Model) :
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_or_create_anonymous_user))
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ("user", "project")

class Issue(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=False)
    description = models.TextField(blank=True)
    user_assigned = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,null=True, related_name='issues_assigned', blank=True)
    status = models.CharField(
        max_length=20,
        choices = [
        ("to_do", "To-do"),
        ("in_progress", "In Progress"),
        ("finished", "Finished")
        ],
        default="to_do"
    )
    tag = models.CharField(
        max_length=20,
        choices = [
        ("bug", "Bug"),
        ("task", "Task"),
        ("feature", "Feature")
        ],
        blank=True
    )
    priority = models.CharField(
        max_length=20,
        choices = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High")
        ],
        blank=True
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_or_create_anonymous_user))
    created_time = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    description = models.TextField(blank=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_or_create_anonymous_user))
    created_time = models.DateTimeField(auto_now_add=True)

