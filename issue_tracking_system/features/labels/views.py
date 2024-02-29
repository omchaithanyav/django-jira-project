from rest_framework import views, permissions, status
from rest_framework.response import Response
from issue_tracking_system.serializers import LabelSerializer
from issue_tracking_system.models import Label, Issue
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class LabelView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        try:
            if pk:
                label = Label.objects.filter(id=pk).first()
                if label is None:
                    return Response({"error": "Label with this id doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
                serializer = LabelSerializer(label)
                return Response(serializer.data, status=status.HTTP_200_OK)

            queryset = Label.objects.all()
            serializer = LabelSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as exception:
            print(f"ERROR: {exception}")

    def delete(self, request, pk=None):
        try:
            label = Label.objects.filter(id=pk).first()
            if label is not None:
                label.delete()
                return Response({"success": "yes"}, status=status.HTTP_200_OK)
            return Response({"error": "The label does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exception:
            print(f"ERROR: {exception}")

    def post(self, request):
        if 'issue' in request.data:
            issue = get_object_or_404(Issue, pk=request.data['issue'])
            data = {'label': request.data['label'],}
            serializer = LabelSerializer(data=data)
            if serializer.is_valid():
                label = serializer.save()
                issue.labels.add(label)
                return Response(LabelSerializer(label).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "No issue id passed"}, status=status.HTTP_400_BAD_REQUEST)
