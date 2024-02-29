"""
URL configuration for django_assignment project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from issue_tracking_system.features.users.views import UserView, LoginView
from issue_tracking_system.features.projects.views import ProjectView
from issue_tracking_system.features.sprints.views import SprintView
from issue_tracking_system.features.labels.views import LabelView
from issue_tracking_system.features.issues.views import IssueView
from issue_tracking_system.features.user_project.views import UserProjectView
from issue_tracking_system.features.watcher.views import WatcherView
from issue_tracking_system.features.comments.views import CommentView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/', UserView.as_view(), name="user"),
    path('api/user/<pk>', UserView.as_view(), name="user with id"),
    path('api/login/', LoginView.as_view(), name="login"),
    path('api/project/', ProjectView.as_view(), name="project"),
    path('api/project/<pk>', ProjectView.as_view(), name="project with id"),
    path('api/sprint/', SprintView.as_view(), name="sprint"),
    path('api/sprint/<pk>', SprintView.as_view(), name="sprint with id"),
    path('api/label/', LabelView.as_view(), name="label"),
    path('api/label/<pk>', LabelView.as_view(), name="label with id"),
    path('api/issue/', IssueView.as_view(), name="issue"),
    path('api/issue/<pk>', IssueView.as_view(), name="issue with id"),
    path('api/userprojectrelation/', UserProjectView.as_view(), name="user project"),
    path('api/userprojectrelation/<pk>', UserProjectView.as_view(), name="user project with project id"),
    path('api/watcher/', WatcherView.as_view(), name="watcher"),
    path('api/watcher/<pk>', WatcherView.as_view(), name="watcher with id"),
    path('api/comment/', CommentView.as_view(), name="comment"),
    path('api/comment/<pk>', CommentView.as_view(), name="comment with id"),
]
