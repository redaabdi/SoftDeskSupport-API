from django.contrib import admin
from django.urls import path, include
from .views import ProfileView, ProjectView, ContributorViewSet, IssueViewSet, CommentViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'projects', ProjectView, basename='project' )
router.register(r'projects/(?P<project_pk>[^/.]+)/issues', IssueViewSet, basename='project-issues')
router.register(r'projects/(?P<project_pk>[^/.]+)/issues/(?P<issue_pk>[^/.]+)/comments', CommentViewSet, basename='project-comments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/signup/', ProfileView.as_view({'post' : 'create'})),
    path('api/profile/', ProfileView.as_view({
        'get' : 'retrieve',
        'put' : 'update',
        'patch' : 'partial_update',
        'delete' : 'destroy'
    })),
    path('api/projects/<int:project_pk>/contributors/', ContributorViewSet.as_view({
        'get': 'list',
        'post': 'create',  
    })
    ),
    path('api/projects/<int:project_pk>/contributors/<int:pk>/', ContributorViewSet.as_view({
        'get': 'retrieve',
        'delete': 'destroy',
    })),

    path('api/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='login_refresh'),
    path('api/', include(router.urls))
]
