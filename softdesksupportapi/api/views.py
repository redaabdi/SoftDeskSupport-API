from rest_framework import viewsets, serializers
from rest_framework import permissions as drf_permissions
from rest_framework.exceptions import PermissionDenied
from .serializers import UserProfileSerializer, ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from .models import Project, Contributor, User, Issue, Comment
from.permissions import IsAuthorOfObject, IsContributorOfProject, IsAuthorOfProject


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

    def get_permissions(self):
        if self.action in ("update", "partial_update", "destroy"):
            classes = [drf_permissions.IsAuthenticated, IsAuthorOfObject]
        else:  # list, retrieve, create
            classes = [drf_permissions.IsAuthenticated]
        return [permission() for permission in classes]
    
    def get_queryset(self):
        return Project.objects.filter(contributor__user=self.request.user)
    
    def perform_create(self, serializer): #override create de la vue
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project)

class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer

    def get_permissions(self):
        if self.action in ("create", "destroy"):
            classes = [drf_permissions.IsAuthenticated, IsAuthorOfProject]
        else:  # list, retrieve
            classes = [drf_permissions.IsAuthenticated, IsContributorOfProject]
        return [permission() for permission in classes]

    def get_queryset(self):
        return Contributor.objects.filter(project=self.kwargs.get('project_pk'))

    def perform_create(self, serializer):
        project = Project.objects.get(pk=self.kwargs.get('project_pk'))
        serializer.save(project=project)
    

class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer

    def get_permissions(self):
        if self.action in ("update", "partial_update", "destroy"):
            classes = [drf_permissions.IsAuthenticated, IsAuthorOfObject]
        else:  # list, retrieve, create
            classes = [drf_permissions.IsAuthenticated, IsContributorOfProject]
        return [permission() for permission in classes]

    def get_queryset(self):
        return Issue.objects.filter(project=self.kwargs.get('project_pk'))

    def perform_create(self, serializer):
        project = Project.objects.get(pk=self.kwargs.get('project_pk'))
        serializer.save(author=self.request.user ,project=project)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ("update", "partial_update", "destroy"):
            classes = [drf_permissions.IsAuthenticated, IsAuthorOfObject]
        else:  # list, retrieve, create
            classes = [drf_permissions.IsAuthenticated, IsContributorOfProject]
        return [permission() for permission in classes]

    def check_issue_belong_project(self) :
        project_pk = self.kwargs.get('project_pk')
        if not Issue.objects.filter(pk=self.kwargs.get('issue_pk'), project_id=project_pk).exists():
            raise PermissionDenied("This issue doesn't exist or belong to the project")

    def get_queryset(self):
        self.check_issue_belong_project()
        issue_pk = self.kwargs.get('issue_pk')
        return Comment.objects.filter(issue=issue_pk)

    def perform_create(self, serializer):
        self.check_issue_belong_project()
        issue_pk = self.kwargs.get('issue_pk')
        issue = Issue.objects.get(pk=issue_pk)
        serializer.save(author=self.request.user ,issue=issue)