from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Project(models.Model):
    # project_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


class UserProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


class Label(models.Model):
    label = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


class Sprint(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="sprints")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    labels = models.ManyToManyField(Label, related_name="sprints", blank=True)


class Issue(models.Model):
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, related_name="issues")
    type = models.CharField(max_length=50, choices=[("story", "Story"), ("task", "Task"), ("bug", "Bug")], default="story")
    title = models.CharField(max_length=150, unique=True)
    status = models.CharField(max_length=50, choices=[("to do", "To Do"), ("in progress", "In Progress"), ("done", "Done")], default="to do")
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="issues")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    labels = models.ManyToManyField(Label, related_name="issues", blank=True)


class Watcher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="watchers")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
