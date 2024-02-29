from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from issue_tracking_system.models import Label, Issue, Project, Sprint


class LabelTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="test_user01", password="test_user01_password")
        self.client.force_authenticate(user=self.user)
        self.label = Label.objects.create(label="Test Label 01")
        self.project = Project.objects.create(name="test_project_02")
        self.sprint = Sprint.objects.create(project=self.project)
        self.issue = Issue.objects.create(sprint=self.sprint, type="task", title="test issue 03", status="to do", assignee=self.user)

    def test_get_labels(self):
        url = reverse('label')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_label(self):
        url = reverse('label with id', kwargs={'pk': self.label.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_label(self):
        data = {'issue': self.issue.id, 'label': self.label.id}
        url = reverse('label')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_label(self):
        url = reverse('label with id', kwargs={'pk': self.label.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
