from rest_framework import generics,permissions, viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import SignupSerializer, UserProfileSerializer, ProjectSerializer
from .models import Project, Contributor


class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]

class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return self.request.user

class ProjectView(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(contributor__user=self.request.user)
    
    def perform_create(self, serializer): #override create de la vue
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project)
    

    
