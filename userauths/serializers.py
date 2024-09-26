from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from userauths import models as use_models


# User Registration Serializer
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = use_models.User
        fields = ('email', 'password', 'password2', 'first_name', 'last_name', 'phone', 'gender', 'is_guest', 'is_host', 'is_admin', 'is_superuser')
        extra_kwargs = {
            'password': {'write_only': True},
            'password2': {'write_only': True},
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data

    def create(self, validated_data):
        user = use_models.User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data['phone'],
            gender=validated_data['gender'],
            is_guest=validated_data['is_guest'],
            is_host=validated_data['is_host'],
            is_admin=validated_data['is_admin'],
            is_superuser=validated_data['is_superuser']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

# User Loggin Serializer
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid email or password.")
        return {'user': user}


# All User List Serializer
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = use_models.User  
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'gender', 'is_guest', 'is_host', 'is_admin', 'is_superuser']
        # fields = '__all__'
