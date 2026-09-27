from rest_framework import viewsets, serializers
from rest_framework import permissions as drf_permissions
from rest_framework.exceptions import PermissionDenied
from .serializers import UserProfileSerializer, ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from .models import Project, Contributor, User, Issue, Comment


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

    def perform_update(self, serializer) :
        if self.request.user != self.get_object().author:
            raise PermissionDenied("Seul l'auteur du projet peut modifier cette ressource")
        serializer.save()

    def perform_destroy(self, instance) :
        if self.request.user != self.get_object().author:
            raise PermissionDenied("Seul l'auteur du projet peut supprimer la ressource")
        instance.delete()

class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [drf_permissions.IsAuthenticated]

    def get_project(self) :
        project_id = self.kwargs.get('project_pk')
        project = Project.objects.get(pk=project_id)
        return project

    def check_is_contributor(self):
        if not Contributor.objects.filter(user=self.request.user, project=self.get_project()).exists():
            raise PermissionDenied("Vous devez être contributeur de ce projet pour y accéder")

    def get_queryset(self):
        self.check_is_contributor()
        return Contributor.objects.filter(project=self.get_project())

    def perform_create(self, serializer):
        if self.request.user != self.get_project().author :
            raise serializers.ValidationError("Vous devez être auteur pour modifier cette ressource")
        serializer.save(project=self.get_project())

    def perform_update(self, serializer) :
        if self.request.user != self.get_project().author:
                raise PermissionDenied("Seul l'auteur du projet peut modifier cette ressource")
        serializer.save()

    def perform_destroy(self, instance) :
        if self.request.user != self.get_project().author:
            raise PermissionDenied("Seul l'auteur du projet peut supprimer la ressource")
        instance.delete()
    

class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [drf_permissions.IsAuthenticated]

    def get_project(self) :
        project_id = self.kwargs.get('project_pk')
        project = Project.objects.get(pk=project_id)
        return project
    
    def check_is_contributor(self):
        if not Contributor.objects.filter(user=self.request.user, project=self.get_project()).exists():
            raise PermissionDenied("Vous devez être contributeur de ce projet pour y accéder")

    def get_queryset(self):
        self.check_is_contributor()
        return Issue.objects.filter(project=self.get_project())

    def perform_create(self, serializer):
        self.check_is_contributor()
        serializer.save(author=self.request.user ,project=self.get_project())

    def perform_update(self, serializer) :
        if self.request.user != self.get_object().author:
            raise PermissionDenied("Seul l'auteur de l'issue peut modifier cette ressource")
        serializer.save()

    def perform_destroy(self, instance) :
        if self.request.user != self.get_object().author:
            raise PermissionDenied("Seul l'auteur de l'issue peut supprimer la ressource")
        instance.delete()

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [drf_permissions.IsAuthenticated]

    def check_is_contributor(self):
        project_pk = self.kwargs.get('project_pk')
        if not Contributor.objects.filter(user=self.request.user, project_id=project_pk).exists():
            raise PermissionDenied("Vous devez être contributeur de ce projet pour y accéder")

    def check_issue_belong_project(self) :
        project_pk = self.kwargs.get('project_pk')
        if not Issue.objects.filter(pk=self.kwargs.get('issue_pk'), project_id=project_pk).exists():
            raise PermissionDenied("This issue doesn't exist or belong to the project")

    def get_queryset(self):
        self.check_is_contributor()
        self.check_issue_belong_project()
        issue_pk = self.kwargs.get('issue_pk')
        return Comment.objects.filter(issue=issue_pk)

    def perform_create(self, serializer):
        self.check_is_contributor()
        self.check_issue_belong_project()
        issue_pk = self.kwargs.get('issue_pk')
        issue = Issue.objects.get(pk=issue_pk)
        serializer.save(author=self.request.user ,issue=issue)

    def perform_update(self, serializer) :
        if self.request.user != self.get_object().author:
            raise PermissionDenied("Seul l'auteur du comment peut modifier cette ressource")
        serializer.save()

    def perform_destroy(self, instance) :
        if self.request.user != self.get_object().author:
            raise PermissionDenied("Seul l'auteur du comment peut supprimer la ressource")
        instance.delete()