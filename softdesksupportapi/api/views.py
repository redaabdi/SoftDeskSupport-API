from rest_framework import generics,permissions, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import SignupSerializer, UserProfileSerializer


class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]

class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return self.request.user

class ProjectView(viewsets.ModelViewSet):
    pass
    
