from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from issue_tracking_system.models import Sprint, Project, Issue


class SprintTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="test_user01", password="test_user01_password")
        self.client.force_authenticate(user=self.user)
        self.project = Project.objects.create(name="test_project_02")
        self.sprint_1 = Sprint.objects.create(project=self.project)
        self.sprint_2 = Sprint.objects.create(project=self.project)
        self.issue_1 = Issue.objects.create(sprint=self.sprint_1, type="task", title="test issue 01", status="to do", assignee=self.user)
        self.issue_2 = Issue.objects.create(sprint=self.sprint_1, type="task", title="test issue 02", status="to do", assignee=self.user)

    def test_get_sprints(self):
        url = reverse('sprint')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_sprint(self):
        url = reverse('sprint with id', kwargs={'pk': self.sprint_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_sprint(self):
        data = {'project': self.project.id, "labels": []}
        url = reverse('sprint')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_sprint(self):
        data = {'sprint': self.sprint_1.id, "issues":[self.issue_1.id, self.issue_2.id]}
        url = reverse('sprint')
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_sprint(self):
        url = reverse('sprint with id', kwargs={'pk': self.sprint_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
