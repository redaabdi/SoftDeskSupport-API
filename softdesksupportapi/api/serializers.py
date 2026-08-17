from rest_framework import serializers
from .models import User, Project

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'can_be_contacted', 'can_data_be_shared', 'age']

    def validate_age(self, value):
        if value < 15:
            raise serializers.ValidationError("Vous devez avoir au moins 15 ans pour vous inscrire.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'can_be_contacted', 'can_data_be_shared', 'age', 'date_joined']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'contributors']
        read_only_fields = ['contributors']

    def validate_contributors(self, value):
        value = [self.request.user]
        return value
    
    def create(self, validated_data) :
        return Project.objects.create(**validated_data)