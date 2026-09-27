from rest_framework import serializers
from .models import User, Project, Contributor, Issue, Comment


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'can_be_contacted', 'can_data_be_shared', 'age','created_time', 'date_joined']

    def validate_age(self, value):
        if value < 15:
            raise serializers.ValidationError("Vous devez avoir au moins 15 ans pour vous inscrire.")
        return value

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data["password"]) #set le password en hashé à l'instance
            validated_data.pop('password') # supprime car le password vient d'etre set, sinon il sera re set mais pas hashé
        return super().update(instance, validated_data) #on rappel le update original mais sans password afin de set le reste
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data) #hasher le mot de passe


class ProjectSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'author', 'type', 'created_time']

class ContributorSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'created_time']
        read_only_fields = ['project']

class IssueSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    user_assigned = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Issue
        fields = ['id', 'author', 'project', "title" ,'description', 'user_assigned', 'status', 'tag', 'priority', 'created_time']
        read_only_fields = ['author','project']

    def validate_user_assigned(self, value):
        project = self.context['view'].get_project()
        if not Contributor.objects.filter(project=project, user=value).exists():
            raise serializers.ValidationError("L'utilisateur doit être contributeur du projet.")
        return value

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'issue', 'description','author', 'created_time']
        read_only_fields = ['author','issue']