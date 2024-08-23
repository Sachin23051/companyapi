from rest_framework import serializers
from .models import Client,Project
from django.contrib.auth.models import User

class ClientSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at','created_by']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']  
  

class ProjectSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(slug_field='client_name', queryset=Client.objects.all())
    users = UserSerializer(many=True, read_only=True)
    user_ids = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True, many=True)
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client', 'users', 'user_ids', 'created_at', 'created_by']

    def create(self, validated_data):
        user_ids = validated_data.pop('user_ids')
        project = Project.objects.create(**validated_data)
        project.users.set(user_ids)  # Add the list of users to the project
        return project