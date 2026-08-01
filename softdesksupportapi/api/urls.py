from django.contrib import admin
from django.urls import path
from .views import PostView

urlpatterns = [
    path('api/', PostView.as_view(), name='post-view'),
    path('admin/', admin.site.urls)
]