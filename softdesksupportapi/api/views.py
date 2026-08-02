from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer


class PostView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "pk"

class SearchPost(APIView):
    # def get(self, request, format=None):
    #     title = request.query_params.get("title", "")
    #     posts = Post.objects.filter(title_icontains=title)
    #     serializer = PostSerializer(posts, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def get (self, request, format=None) :
        # Get the title from the query parameters (if none, default to empty string)
        title = request.query_params.get("title", "")
        if title:
            posts = Post.objects.filter(title__icontains=title)
        else:
            posts = Post.objects.all()

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status. HTTP_200_OK)