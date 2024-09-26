from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login
from userauths import serializers as userauth_serializers
from userauths import models as userauth_models


# User Register View
class UserRegisterView(generics.CreateAPIView):
    queryset = userauth_models.User.objects.all()
    serializer_class = userauth_serializers.UserRegisterSerializer


# User Loggin View
class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = userauth_serializers.UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)  # Use Django's login function
        return Response({"message": "Login successful."}, status=status.HTTP_200_OK)
    
# ALl User List View    
class UserListView(generics.ListAPIView):
    queryset = userauth_models.User.objects.all()
    serializer_class = userauth_serializers.UserListSerializer
