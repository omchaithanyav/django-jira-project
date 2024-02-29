from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User


class UserTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="test_user01", password="test_user01_password")
        self.client.force_authenticate(user=self.user)

    def test_get_users(self):
        url = reverse('user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user(self):
        url = reverse('user with id', kwargs={'pk': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_user(self):
        data = {'username': 'test_username', 'password': 'test_password'}
        url = reverse('login')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_user(self):
        url = reverse('user with id', kwargs={'pk': self.user.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
