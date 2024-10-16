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

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = use_models.User
        fields = ['id', 'username', 'email', 'first_name', 'last_name'] 


# All User List Serializer
# class UserListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = use_models.User  
#         fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'gender', 'is_guest', 'is_host', 'is_admin', 'is_superuser']
#         # fields = '__all__'

class UserListSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = use_models.User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'gender', 'is_guest', 'is_host', 'is_admin', 'is_superuser', 'role']

    def get_role(self, obj):
        roles = []
        if obj.is_guest:
            roles.append("Guest")
        if obj.is_host:
            roles.append("Host")
        if obj.is_admin:
            roles.append("Admin")
        if obj.is_superuser:
            roles.append("Superuser")
        
        return ", ".join(roles) if roles else "No Role"


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = use_models.Profile
        fields = ['profile_picture', 'date_of_birth', 'address', 'bio', 'identity_type', 'identity_image', 'verified']



class UserUpdateSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    role = serializers.SerializerMethodField()

    class Meta:
        model = use_models.User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'gender', 'is_guest', 'is_host', 'is_admin', 'is_superuser', 'profile', 'role']

    # Get the Use Role like..(Host, Guest, Admin, Superuser)
    def get_role(self, obj):
        roles = []
        if obj.is_guest:
            roles.append("Guest")
        if obj.is_host:
            roles.append("Host")
        if obj.is_admin:
            roles.append("Admin")
        if obj.is_superuser:
            roles.append("Superuser")
        return ", ".join(roles) if roles else "No Role"

    # Ensure that the identity image is provided only if an identity type is selected.
    def validate(self, data):
        profile_data = data.get('profile', {})
        identity_type = profile_data.get('identity_type')
        identity_image = profile_data.get('identity_image')

        # If identity image is provided, check if identity type is also provided
        if identity_image and not identity_type:
            raise serializers.ValidationError("Please select an identity type before uploading the identity document.")

        # If identity type is selected, ensure identity image is provided
        if identity_type and not identity_image:
            raise serializers.ValidationError("Identity image must be provided if identity type is selected.")

        return data

    def update(self, instance, validated_data):
        # Update User fields
        profile_data = validated_data.pop('profile', None)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.is_guest = validated_data.get('is_guest', instance.is_guest)
        instance.is_host = validated_data.get('is_host', instance.is_host)
        instance.is_admin = validated_data.get('is_admin', instance.is_admin)
        instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
        instance.save()

        # Update Profile fields if profile data is present
        if profile_data:
            profile = instance.profile
            profile.profile_picture = profile_data.get('profile_picture', profile.profile_picture)
            profile.date_of_birth = profile_data.get('date_of_birth', profile.date_of_birth)
            profile.address = profile_data.get('address', profile.address)
            profile.bio = profile_data.get('bio', profile.bio)
            profile.identity_type = profile_data.get('identity_type', profile.identity_type)
            profile.identity_image = profile_data.get('identity_image', profile.identity_image)
            
            # Verify the profile if identity image is provided
            if 'identity_image' in profile_data and profile_data['identity_image'] is not None:
                profile.verified = True
            else:
                profile.verified = False
            
            profile.save()

        return instance