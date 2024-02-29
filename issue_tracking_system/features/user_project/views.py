from rest_framework import views, permissions, status
from rest_framework.response import Response
from issue_tracking_system.serializers import UserProjectSerializer
from issue_tracking_system.models import UserProject, Project
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class UserProjectView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            project_id = request.data.get('project')
            user_ids = request.data.get('user')
            project = Project.objects.filter(id=project_id).first()
            user_project_relations = []
            for user_id in user_ids:
                user = User.objects.filter(id=user_id).first()
                user_project = UserProject.objects.create(user=user, project=project, is_active=True)
                serializer = UserProjectSerializer(user_project)
                user_project_relations.append(serializer.data)
            return Response({"success": "True", "data": user_project_relations}, status=status.HTTP_201_CREATED)
        except Exception as exception:
            print(f"ERROR: {exception}")
            return Response({f"success": "False"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        try:
            if pk:
                project = Project.objects.filter(id=pk).first()
                if project is None:
                    return Response({"error": "No Project present for the given id"}, status=status.HTTP_400_BAD_REQUEST)
                user_project = UserProject.objects.filter(project=project)
                if user_project is None:
                    return Response({"error": "No User Project Relation present for this project"}, status=status.HTTP_400_BAD_REQUEST)
                serializer = UserProjectSerializer(user_project, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            queryset = UserProject.objects.all()
            serializer = UserProjectSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as exception:
            print(f"ERROR: {exception}")

    def put(self, request, *args, **kwargs):
        try:
            project_id = request.data.get("project")
            user_id = request.data.get("user")
            user = User.objects.filter(id=user_id).first()
            project = Project.objects.filter(id=project_id).first()
            user_project = UserProject.objects.filter(project=project, user=user).first()
            if user_project is None:
                return Response({"error": "No User Project Relation present for this project"}, status=status.HTTP_400_BAD_REQUEST)
            user_project.is_active = not user_project.is_active
            user_project.save()
            serializer = UserProjectSerializer(user_project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as exception:
            print(f"ERROR: {exception}")

    def delete(self, request, pk=None):
        try:
            user_project = UserProject.objects.filter(id=pk)
            if user_project is not None:
                user_project.delete()
                return Response({"success": "yes"}, status=status.HTTP_200_OK)
            return Response({"error": "The user project relation does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exception:
            print(f"ERROR: {exception}")
