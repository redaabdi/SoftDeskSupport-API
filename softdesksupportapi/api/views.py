from rest_framework import viewsets, serializers
from rest_framework import permissions as drf_permissions
from .serializers import UserProfileSerializer, ProjectSerializer, ContributorSerializer
from .models import Project, Contributor, User
from django.shortcuts import get_object_or_404


class ProfileView(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer

    def get_permissions(self):
        if self.action == "create":
            return [drf_permissions.AllowAny()]
        return [drf_permissions.IsAuthenticated()]

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def get_object(self):
        # Ne va pas chercher le pk dans l'url mais agit sur le user directement
        return self.request.user


class ProjectView(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [drf_permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(contributor__user=self.request.user)
    
    def perform_create(self, serializer): #override create de la vue
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project)

class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [drf_permissions.IsAuthenticated]

    def get_project(self) :
        project_id = self.kwargs.get('project_pk')
        project = Project.objects.get(contributor__user=self.request.user, pk=project_id)
        return project

    def get_queryset(self):
        project = self.get_project()
        return Contributor.objects.filter(project=project)

    def perform_create(self, serializer):
        project = self.get_project()
        if self.request.user != project.author :
            raise serializers.ValidationError("Vous devez être auteur pour modifier cette ressource")
        # if Contributor.objects.filter(project=project, user=).exists():
        #     raise serializers.ValidationError("Cet utilisateur est déjà contributeur de ce projet.")
        serializer.save(project=project)





    
