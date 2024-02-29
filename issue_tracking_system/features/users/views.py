from django.contrib.auth.models import User
from rest_framework import views, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from issue_tracking_system.serializers import UserSerializer


class UserView(views.APIView):

    def get(self, request, pk=None):
        try:
            if pk:
                # user = get_object_or_404(User, id=pk)
                user = User.objects.filter(id=pk).first()
                if user is None:
                    return Response({"error": "User with this id doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)

            queryset = User.objects.all()
            serializer = UserSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as exception:
            print(f"ERROR: {exception}")

    def delete(self, request, pk=None):
        try:
            user = User.objects.filter(id=pk).first()
            if user is not None:
                user.delete()
                return Response({"success": "yes"}, status=status.HTTP_200_OK)
            return Response({"error": "The user does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exception:
            print(f"ERROR: {exception}")


class LoginView(views.APIView):

    def post(self, request, *args, **kwargs):
        try:
            print(f"REQUEST: {request}")
            username = request.data.get('username')
            password = request.data.get('password')

            if not username or not password:
                return Response({'detail': 'Username and password required'},
                                status=status.HTTP_400_BAD_REQUEST)

            # user = authenticate(request, username=username, password=password) # returns None if wrong password else returns user object.
            user = User.objects.filter(username=username).first()
            if user:
                if not user.check_password(password):
                    return Response({"password": ["Wrong password."]}, status=status.HTTP_401_UNAUTHORIZED)

                refresh_token = RefreshToken.for_user(user)
                return Response({
                    "status": "success",
                    "code": 200,
                    "token": str(refresh_token.access_token)
                }, status=status.HTTP_200_OK)

            else:
                serializer = UserSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    user = serializer.save()
                    refresh_token = RefreshToken.for_user(user)
                    return Response({
                        'token': str(refresh_token.access_token),
                        'data': serializer.data
                    }, status=status.HTTP_201_CREATED)
        except Exception as exception:
            print(f"ERROR: {exception}")
