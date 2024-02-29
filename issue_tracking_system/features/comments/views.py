from rest_framework import views, permissions, status
from rest_framework.response import Response
from issue_tracking_system.serializers import CommentSerializer
from issue_tracking_system.models import Comment, Issue, UserProject
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class CommentView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            issue_id = request.data.get("issue")
            user_id = request.data.get("user")
            comment = request.data.get("comment")
            issue = Issue.objects.filter(id=issue_id).select_related("sprint__project").first()
            if issue is None:
                return Response({'error': 'The issue does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            project = issue.sprint.project
            user_project = UserProject.objects.filter(project=project, user__id=user_id).first()
            if user_project is None:
                return Response({'error': 'User is not a part of this project'}, status=status.HTTP_400_BAD_REQUEST)

            if not user_project.is_active:
                return Response({'error': 'User is not active in this project'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as exception:
            print(f"ERROR: {exception}")

    def get(self, request):
        try:
            queryset = Comment.objects.all()
            serializer = CommentSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as exception:
            print(f"ERROR: {exception}")

    def delete(self, request, pk=None):
        try:
            comment = Comment.objects.filter(id=pk).first()
            if comment is not None:
                comment.delete()
                return Response({"success": "yes"}, status=status.HTTP_200_OK)
            return Response({"error": "The comment does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exception:
            print(f"ERROR: {exception}")
