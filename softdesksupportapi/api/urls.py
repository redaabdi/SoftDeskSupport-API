from django.contrib import admin
from django.urls import path
from .views import PostView, PostUpdateDelete, SearchPost

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', PostView.as_view(), name='post-view'),
    path('api/<int:pk>', PostUpdateDelete.as_view(), name='post-update-delete'),
    path('api/search', SearchPost.as_view(), name='search-post')
]