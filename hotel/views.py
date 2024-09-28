from rest_framework import generics, status, permissions
# from .models import Property
from hotel import models as hotel_models
# from .serializers import PropertySerializer
from hotel import serializers as hotel_serializers
from userauths import permissions as user_permission
from rest_framework.response import Response



# List all properties and Create a new property
class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = hotel_models.Property.objects.all()
    serializer_class = hotel_serializers.PropertySerializer

    # For Filter the Property by using the email. (GET /properties/?email=example@example.com)
    def get_queryset(self):
        queryset = hotel_models.Property.objects.all()
        email = self.request.query_params.get('email', None)
        if email:
            queryset = queryset.filter(email__icontains=email)
        return queryset

    # Custom permission logic for creating properties (POST request)
    # def post(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated:
    #         return Response({"error": "You must be authenticated to add properties."}, status=status.HTTP_403_FORBIDDEN)
        
    #     # Checking if the user is a HostUser, Admin, or SuperUser
    #     if not (user_permission.IsHostUser.has_permission(self, request, self) or 
    #             user_permission.IsAdminUser.has_permission(self, request, self) or 
    #             user_permission.IsSuperUser.has_permission(self, request, self)):
    #         return Response({"error": "You do not have permission to create properties."}, status=status.HTTP_403_FORBIDDEN)
        
    #     # If the user has the necessary permissions, allow the creation
    #     return super().post(request, *args, **kwargs)

# Retrieve, Update, and Delete a specific property
class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = hotel_models.Property.objects.all()
    serializer_class = hotel_serializers.PropertySerializer


# List all room by the Property and create new room for property
class RoomListCreateView(generics.ListCreateAPIView):
    queryset = hotel_models.Room.objects.all()
    serializer_class = hotel_serializers.RoomSerializer


# Retrive, Update, and Delete a specific Room
class RoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = hotel_models.Room.objects.all()
    serializer_class = hotel_serializers.RoomSerializer

# List/Create all Amenities by the Property and the Room
class RoomAmenitiesListCreateView(generics.ListCreateAPIView):
    queryset = hotel_models.RoomAmenities.objects.all()
    serializer_class = hotel_serializers.RoomAmenitiesSerializer

# Retrive, Update and Delete a Specific Amenities
class RoomAmenitiesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = hotel_models.RoomAmenities.objects.all()
    serializer_class = hotel_serializers.RoomAmenitiesSerializer