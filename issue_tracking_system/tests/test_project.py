from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from issue_tracking_system.models import Project
from django.contrib.auth.models import User


class ProjectTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="test_user01", password="test_user01_password")
        self.client.force_authenticate(user=self.user)
        self.project = Project.objects.create(name="test_project_01")

    def test_get_projects(self):
        url = reverse('project')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_project(self):
        url = reverse('project with id', kwargs={'pk': self.project.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_project(self):
        data = {'name': 'Test Project 2'}
        url = reverse('project')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_project(self):
        data = {'name': 'Project 1 Updated'}
        url = reverse('project with id', kwargs={'pk': self.project.id})
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_project(self):
        url = reverse('project with id', kwargs={'pk': self.project.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
