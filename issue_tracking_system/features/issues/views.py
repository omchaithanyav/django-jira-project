from rest_framework import views, permissions, status
from rest_framework.response import Response
from issue_tracking_system.serializers import IssueSerializer
from issue_tracking_system.models import Issue, Project, UserProject
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class IssueView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            serializer = IssueSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as exception:
            print(f"ERROR: {exception}")

    def delete(self, request, pk=None):
        try:
            issue = Issue.objects.filter(id=pk).first()
            if issue is not None:
                issue.delete()
                return Response({"success": "yes"}, status=status.HTTP_200_OK)
            return Response({"error": "The issue does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exception:
            print(f"ERROR: {exception}")

    def get(self, request):
        try:
            page_number = request.GET.get('page')
            project_id = request.GET.get('project')
            user_id = request.GET.get('assignee')

            if not page_number:
                return Response({"error": "Page param not passed"}, status=status.HTTP_400_BAD_REQUEST)

            if project_id:
                project = get_object_or_404(Project, id=project_id)
                issues = Issue.objects.filter(sprint__project=project).order_by('-updated_at')
                if issues is None:
                    return Response({"error": "No issues present for this project"}, status=status.HTTP_400_BAD_REQUEST)
                paginator = Paginator(issues, 50)
                try:
                    issues_in_page = paginator.page(page_number)
                except EmptyPage:
                    return Response({"error": "Page doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
                serializer = IssueSerializer(issues_in_page, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            if user_id:
                issues = Issue.objects.filter(assignee__id=user_id).order_by('-updated_at')
                if issues is None:
                    return Response({"error": "No issues assigned to this assignee"}, status=status.HTTP_400_BAD_REQUEST)
                paginator = Paginator(issues, 50)
                try:
                    issues_in_page = paginator.page(page_number)
                except EmptyPage:
                    return Response({"error": "Page doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
                serializer = IssueSerializer(issues_in_page, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response({"error": "Project/Assignee param is not passed"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as exception:
            print(f"ERROR: {exception}")

    def put(self, request, pk=None):
        try:
            issue = Issue.objects.filter(id=pk).first()
            if issue is None:
                return Response({'error': 'The issue does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            issue_status = request.data.get('status')
            user_id = request.data.get("assignee")

            if issue_status:
                if issue_status not in [choice[0] for choice in Issue.status.field.choices] or issue.status == issue_status:
                    return Response({"error": "Params not passed properly"}, status=status.HTTP_400_BAD_REQUEST)
                issue.status = issue_status
                issue.save()
                serializer = IssueSerializer(issue)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            if user_id:
                assignee = User.objects.filter(id=user_id).first()
                user_project = UserProject.objects.filter(user=assignee, project=issue.sprint.project).first()
                if user_project is None:
                    return Response({'error': 'User is not a part of this project'}, status=status.HTTP_400_BAD_REQUEST)
                if user_project.is_active is False:
                    return Response({'error': 'User is not active in this project'}, status=status.HTTP_400_BAD_REQUEST)
                issue.assignee = assignee
                issue.save()
                serializer = IssueSerializer(issue)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"error": "Params not passed properly"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exception:
            print(f"ERROR: {exception}")
