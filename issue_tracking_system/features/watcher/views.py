from rest_framework import views, permissions, status
from rest_framework.response import Response
from issue_tracking_system.serializers import WatcherSerializer
from issue_tracking_system.models import Watcher, Issue, UserProject
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class WatcherView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        issue_id = request.data.get("issue")
        user_id = request.data.get("user")

        issue = Issue.objects.filter(id=issue_id).select_related("sprint__project").first()
        if issue is None:
            Response({'error': 'The issue does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        project = issue.sprint.project
        user_project = UserProject.objects.filter(project=project, user__id=user_id).first()
        if user_project is None:
            return Response({'error': 'User is not a part of this project'}, status=status.HTTP_400_BAD_REQUEST)

        if not user_project.is_active:
            Response({'error': 'User is not active in this project'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = WatcherSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        try:
            queryset = Watcher.objects.all()
            serializer = WatcherSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as exception:
            print(f"ERROR: {exception}")

    def put(self, request, *args, **kwargs):
        try:
            user_id = request.data.get("user")
            issue_id = request.data.get("issue")

            watcher = Watcher.objects.filter(user__id=user_id, issue__id=issue_id).first()
            if watcher is None:
                return Response({"Watcher with the give ID is not found"}, status=status)
            watcher.is_active = not watcher.is_active
            watcher.save()
            serializer = WatcherSerializer(watcher)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as exception:
            print(f"ERROR: {exception}")

    def delete(self, request, pk=None):
        try:
            watcher = Watcher.objects.filter(id=pk)
            if watcher is not None:
                watcher.delete()
                return Response({"success": "yes"}, status=status.HTTP_200_OK)
            return Response({"error": "The watcher does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exception:
            print(f"ERROR: {exception}")
