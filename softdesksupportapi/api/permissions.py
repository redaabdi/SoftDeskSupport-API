from rest_framework import permissions
from .models import Contributor, Project

class IsAuthorOfObject(permissions.BasePermission):
    message = "Vous n'êtes pas auteur de cet objet."

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

class IsAuthorOfProject(permissions.BasePermission):
    message = "Vous n'êtes pas auteur de ce projet."

    def has_permission(self, request, view):
        return Project.objects.filter(
            pk=view.kwargs["project_pk"], author=request.user
            ).exists()

class IsContributorOfProject(permissions.BasePermission):
    message = "Vous n'êtes pas contributeur de ce projet."

    def has_permission(self, request, view):
        return Contributor.objects.filter(
            user=request.user, project_id=view.kwargs["project_pk"]
        ).exists()