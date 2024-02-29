from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from issue_tracking_system.models import Project, Sprint, Comment, Issue, UserProject


class CommentTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="test_user01", password="test_user01_password")
        self.client.force_authenticate(user=self.user)
        self.project = Project.objects.create(name="test_project_02")
        self.user_project = UserProject.objects.create(user=self.user, project=self.project)
        self.sprint = Sprint.objects.create(project=self.project)
        self.issue = Issue.objects.create(sprint=self.sprint, type="task", title="test issue 01", status="to do",assignee=self.user)
        self.comment = Comment.objects.create(comment="test comment 1", user=self.user, issue=self.issue)

    def test_get_comments(self):
        url = reverse('comment')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_comment(self):
        data = {'comment': "Test Comment 2", 'user': self.user.id, 'issue':self.issue.id}
        url = reverse('comment')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_comment(self):
        url = reverse('comment with id', kwargs={'pk': self.comment.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
