from rest_framework import generics, viewsets
from rest_framework import permissions as drf_permissions
from .serializers import UserProfileSerializer, ProjectSerializer
from .models import Project, Contributor, User
from django.shortcuts import get_object_or_404


# class SignupView(generics.CreateAPIView):
#     serializer_class = SignupSerializer
#     permission_classes = [permissions.AllowAny]

# class ProfileView(generics.RetrieveAPIView):
#     serializer_class = UserProfileSerializer
#     permission_classes = [IsAuthenticated]
#     def get_object(self):
#         return self.request.user

class ProjectView(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [drf_permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(contributor__user=self.request.user)
    
    def perform_create(self, serializer): #override create de la vue
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project)

class ProfileView(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer

    def get_permissions(self):
        if self.action == "create":
            return [drf_permissions.AllowAny()]
        return [drf_permissions.IsAuthenticated()]

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)
    
    def get_object(self):
        # No pk in the URL — always act on the current user's own profile
        return self.request.user





    
