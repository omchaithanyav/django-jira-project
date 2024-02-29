from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from issue_tracking_system.models import Project, Sprint, UserProject


class UserProjectTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_1 = User.objects.create_user(username="test_user01", password="test_user01_password")
        self.user_2 = User.objects.create_user(username="test_user02", password="test_user02_password")
        self.client.force_authenticate(user=self.user_1)
        self.project = Project.objects.create(name="test_project_06")
        self.user_project = UserProject.objects.create(user=self.user_1, project=self.project)

    def test_get_user_projects(self):
        url = reverse('user project')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_project(self):
        url = reverse('user project with project id', kwargs={'pk': self.project.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_user_project(self):
        data = {'project': self.project.id, 'user': [self.user_2.id]}
        url = reverse('user project')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_user_project(self):
        data = {'project': self.project.id, 'user': self.user_1.id}
        url = reverse('user project')
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_user_project(self):
        url = reverse('user project with project id', kwargs={'pk': self.user_project.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
