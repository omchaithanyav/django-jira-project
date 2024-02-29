from rest_framework import views, permissions, status
from rest_framework.response import Response
from issue_tracking_system.serializers import ProjectSerializer
from issue_tracking_system.models import Project
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class ProjectView(views.APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        try:
            if pk:
                # project = get_object_or_404(Project, id=pk)
                project = Project.objects.filter(id=pk).first()
                if project is None:
                    return Response({"error": "Project with this id doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
                serializer = ProjectSerializer(project)
                return Response(serializer.data, status=status.HTTP_200_OK)

            queryset = Project.objects.all()
            serializer = ProjectSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as exception:
            print(f"ERROR: {exception}")

    def post(self, request, *args, **kwargs):
        try:
            if "name" in request.data and request.data.get("name").strip():
                serializer = ProjectSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    project = serializer.save()
                    data = serializer.data
                    return Response(data, status=status.HTTP_201_CREATED)
            return Response({ "name": [ "This field may not be blank."] }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exception:
            print(f"ERROR: {exception}")

    def delete(self, request, pk=None):
        try:
            project = Project.objects.filter(id=pk).first()
            if project is not None:
                project.delete()
                return Response({"success": "yes"}, status=status.HTTP_200_OK)
            return Response({"error": "The project does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exception:
            print(f"ERROR: {exception}")

    def put(self, request, pk=None):
        try:
            if pk:
                project = Project.objects.filter(id=pk).first()
                if project is not None:
                    serializer = ProjectSerializer(project, data=request.data)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response({"error": "The project does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exception:
            print(f"ERROR: {exception}")
