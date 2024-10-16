from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login
from userauths import serializers as userauth_serializers
from userauths import models as userauth_models
import logging
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    Custom session authentication class that disables CSRF checks.
    """
    def enforce_csrf(self, request):
        # This method is overridden to skip CSRF validation.
        return


# User Register View
class UserRegisterView(generics.CreateAPIView):
    queryset = userauth_models.User.objects.all()
    serializer_class = userauth_serializers.UserRegisterSerializer
    authentication_classes = [CsrfExemptSessionAuthentication]


# User Loggin View
class UserLoginView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    def post(self, request, *args, **kwargs):
        serializer = userauth_serializers.UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)  # Use Django's login function
        login_user_email = user.email
        print('****************************************')
        print('Login_User_Email:', login_user_email)
        print('****************************************')
        return Response({"message": "Login successful."}, status=status.HTTP_200_OK)
    
# ALl User List View    
class UserListView(generics.ListAPIView):
    queryset = userauth_models.User.objects.all()
    serializer_class = userauth_serializers.UserListSerializer



logger = logging.getLogger(__name__)
class UserUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = userauth_models.User.objects.all()
    serializer_class = userauth_serializers.UserListSerializer
    # Use the custom session authentication without CSRF check
    authentication_classes = [CsrfExemptSessionAuthentication]


    def put(self, request, *args, **kwargs):
        logger.debug(f'Request method: {request.method}')
        return self.update(request, *args, **kwargs)

    # def patch(self, request, *args, **kwargs):
    #     logger.debug(f'Request method: {request.method}')
    #     return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        logger.debug(f'Request method: {request.method}')
        # Set partial=True to allow partial updates
        return self.partial_update(request, *args, **kwargs)
    

class UserProfileUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = userauth_models.User.objects.all()
    serializer_class = userauth_serializers.UserUpdateSerializer
    authentication_classes = [CsrfExemptSessionAuthentication]

    def put(self, request, *args, **kwargs):
        logger.debug(f"Request data: {request.data}")
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        logger.debug(f"Request data: {request.data}")
        return self.partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Override to ensure both User and Profile are updated."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()  # Get the user object

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)