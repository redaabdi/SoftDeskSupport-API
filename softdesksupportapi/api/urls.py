from django.contrib import admin
from django.urls import path, include
from .views import ProfileView, ProjectView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('projects', ProjectView, basename='project' )
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/signup/', SignupView.as_view(), name='signup'),
    path('api/signup/', ProfileView.as_view({'post' : 'create'})),
    path('api/profile/', ProfileView.as_view({
        'get' : 'list',
        'put' : 'update',
        'patch' : 'partial_update',
        'delete' : 'destroy'
    })),
    path('api/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='login_refresh'),
    # path('api/profile/', ProfileView.as_view(), name='profile'),
    path('api/', include(router.urls))
]