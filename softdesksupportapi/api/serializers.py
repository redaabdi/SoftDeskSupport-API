from rest_framework import serializers
from .models import User, Project, Contributor


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'can_be_contacted', 'can_data_be_shared', 'age', 'date_joined']

    def validate_age(self, value):
        if value < 15:
            raise serializers.ValidationError("Vous devez avoir au moins 15 ans pour vous inscrire.")
        return value
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data) #hasher le mot de passe


class ProjectSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'author', 'type']

class ContributorSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project']
        read_only_fields = ['project']
