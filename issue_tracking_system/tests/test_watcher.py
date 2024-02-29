from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from issue_tracking_system.models import Watcher, Issue, Project, Sprint, UserProject


class WatcherTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="test_user05", password="test_user05_password")
        self.client.force_authenticate(user=self.user)
        self.project = Project.objects.create(name="test_project_06")
        self.user_project = UserProject.objects.create(user=self.user, project=self.project)
        self.sprint = Sprint.objects.create(project=self.project)
        self.issue = Issue.objects.create(sprint=self.sprint, type="task", title="test issue 09", status="to do", assignee=self.user)
        self.watcher = Watcher.objects.create(user=self.user, issue=self.issue)

    def test_get_watchers(self):
        url = reverse('watcher')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_watcher(self):
        data = {'issue': self.issue.id, 'user': self.user.id}
        url = reverse('watcher')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_watcher(self):
        params = {'user': self.user.id, 'issue': self.issue.id}
        url = reverse('watcher')
        response = self.client.put(url, params, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_watcher(self):
        url = reverse('watcher with id', kwargs={'pk': self.watcher.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
