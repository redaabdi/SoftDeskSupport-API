from rest_framework import generics,permissions, viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import SignupSerializer, UserProfileSerializer, ProjectSerializer
from .models import Project


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
        Project.objects.filter(contributors=self.request.user)

    
