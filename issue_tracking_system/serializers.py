from django.contrib.auth.models import User
from rest_framework import serializers
from issue_tracking_system.models import Project, Sprint, Label, Issue, UserProject, Watcher, Comment
from datetime import datetime


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.updated_at = datetime.now()
        instance.save()
        return instance


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'type', 'status', 'sprint', 'assignee', 'created_at', 'updated_at']


class LabelSerializer(serializers.ModelSerializer):
    issues = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Label
        fields = ['id', 'label', 'issues', 'created_at', 'updated_at']

class SprintSerializer(serializers.ModelSerializer):
    labels = serializers.SlugRelatedField(many=True, slug_field='label', queryset=Label.objects.all())

    class Meta:
        model = Sprint
        fields = "__all__"

class UserProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProject
        fields = "__all__"

class WatcherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watcher
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
