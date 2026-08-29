from django.contrib import admin
from django.urls import path, include
from .views import ProfileView, ProjectView, ContributorViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'projects', ProjectView, basename='project' )
router.register(r'projects/(?P<project_pk>[^/.]+)/contributors', ContributorViewSet, basename='project-contributors')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/signup/', ProfileView.as_view({'post' : 'create'})),
    path('api/profile/', ProfileView.as_view({
        'get' : 'list',
        'put' : 'update',
        'patch' : 'partial_update',
        'delete' : 'destroy'
    })),
    path('api/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='login_refresh'),
    path('api/', include(router.urls))
]