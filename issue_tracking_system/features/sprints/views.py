from rest_framework import views, permissions, status
from rest_framework.response import Response
from issue_tracking_system.serializers import SprintSerializer
from issue_tracking_system.models import Sprint, Issue
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class SprintView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        try:
            if pk:
                sprint = Sprint.objects.filter(id=pk).first()
                if sprint is None:
                    return Response({"error": "Sprint with the given id doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
                serializer = SprintSerializer(sprint)
                return Response(serializer.data, status=status.HTTP_200_OK)

            queryset = Sprint.objects.all()
            serializer = SprintSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as exception:
            print(f"ERROR: {exception}")

    def post(self, request, *args, **kwargs):
        try:
            serializer = SprintSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as exception:
            print(f"ERROR: {exception}")

    def delete(self, request, pk=None):
        try:
            sprint = Sprint.objects.filter(id=pk).first()
            if sprint is not None:
                sprint.delete()
                return Response({"success": "yes"}, status=status.HTTP_200_OK)
            return Response({"error": "The sprint does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exception:
            print(f"ERROR: {exception}")

    def put(self, request):
        try:
            sprint_id = request.data.get('sprint')
            issue_ids = request.data.get('issues')
            if not sprint_id:
                return Response({"error": "No sprint id passed"}, status=status.HTTP_400_BAD_REQUEST)
            if not issue_ids:
                return Response({"error": "No issue ids passed"}, status=status.HTTP_400_BAD_REQUEST)
            sprint = Sprint.objects.filter(id=sprint_id).first()
            if sprint is None:
                return Response({"error": "Sprint with the given id doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
            issues = Issue.objects.filter(id__in=issue_ids)
            nonexistent_issues = set(issue_ids) - set(issue.id for issue in issues)
            if nonexistent_issues:
                return Response({"error": f"Issues don't exist for the given issue ids{list(nonexistent_issues)}"}, status=status.HTTP_400_BAD_REQUEST)
            issues.update(sprint=sprint)
            return Response({"success": "True"}, status=status.HTTP_201_CREATED)
        except Exception as exception:
            print(f"ERROR: {exception}")
