from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from issue_tracking_system.models import Sprint, Project, Issue, UserProject


class IssueTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="test_user01", password="test_user01_password")
        self.client.force_authenticate(user=self.user)
        self.project = Project.objects.create(name="test_project_02")
        self.user_project = UserProject.objects.create(user=self.user, project=self.project)
        self.sprint = Sprint.objects.create(project=self.project)
        self.issue = Issue.objects.create(sprint=self.sprint, type="task", title="test issue 01", status="to do", assignee=self.user)

    def test_get_issues_assignee(self):
        url = reverse('issue')
        params = {"page":1, "assignee":self.user.id}
        response = self.client.get(url, params, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_issues_project(self):
        url = reverse('issue')
        params = {"page":1, "project":self.project.id}
        response = self.client.get(url, params, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_issue(self):
        data = {"sprint":self.sprint.id, "type":"task", "title":"test issue 03", "status":"to do", "assignee":self.user.id}
        url = reverse('issue')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_issue_status(self):
        params = {'status': 'done'}
        url = reverse('issue with id', kwargs={'pk': self.issue.id})
        response = self.client.put(url, params, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_issue_assignee(self):
        params = {'assignee': self.user.id}
        url = reverse('issue with id', kwargs={'pk': self.issue.id})
        response = self.client.put(url, params, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_issue(self):
        url = reverse('issue with id', kwargs={'pk': self.issue.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
