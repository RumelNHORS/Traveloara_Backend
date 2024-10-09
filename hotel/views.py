from rest_framework import generics, status, permissions
# from .models import Property
from hotel import models as hotel_models
# from .serializers import PropertySerializer
from hotel import serializers as hotel_serializers
from userauths import permissions as user_permission
from rest_framework.response import Response
from django.utils.dateparse import parse_date
from rest_framework.exceptions import ValidationError
from django.utils import timezone



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
# class RoomListCreateView(generics.ListCreateAPIView):
#     queryset = hotel_models.Room.objects.all()
#     serializer_class = hotel_serializers.RoomSerializer

class RoomListCreateView(generics.ListCreateAPIView):
    queryset = hotel_models.Room.objects.all()
    serializer_class = hotel_serializers.RoomSerializer

    # For filtering the rooms by User ID, Property ID, City, and Room Capacity
    def get_queryset(self):
        queryset = hotel_models.Room.objects.all()

        # Get user_id from query parameters
        user_id = self.request.query_params.get('user_id', None)
        # Get property_id from the query parameters
        property_id = self.request.query_params.get('property_id', None)

        city = self.request.query_params.get('city', None)
        room_capacity = self.request.query_params.get('room_capacity', None)

        # Boolean field filters
        is_available = self.request.query_params.get('is_available', None)
        is_smoking = self.request.query_params.get('is_smoking', None)
        is_media = self.request.query_params.get('is_media', None)
        is_event = self.request.query_params.get('is_event', None)
        is_unmarried = self.request.query_params.get('is_unmarried', None)
        is_pet = self.request.query_params.get('is_pet', None)

        if user_id:
            # Filter rooms by the provided user_id from the Property model(GET /rooms/?user_id=11)
            queryset = queryset.filter(property__user_id=user_id)
        
        # Filter rooms by property_id if provided (GET /rooms/?property_id=5)
        if property_id:
            queryset = queryset.filter(property_id=property_id)
        
        # Filter by city if provided
        if city:
            queryset = queryset.filter(property__city__icontains=city)

        # Filter by room capacity if provided (?room_capacity=3)
        if room_capacity:
            queryset = queryset.filter(room_capacity__gte=room_capacity)

        # Filter the room by the room and the room capacity (?city=dhaka&room_capacity=3)
        
        # [?is_available=True&is_smoking=True&is_media=False]
        # Filter by is_available if provided
        if is_available is not None:
            queryset = queryset.filter(is_available=is_available)

        # Filter by is_smoking if provided
        if is_smoking is not None:
            queryset = queryset.filter(is_smoking=is_smoking)

        # Filter by is_media if provided
        if is_media is not None:
            queryset = queryset.filter(is_media=is_media)

        # Filter by is_event if provided
        if is_event is not None:
            queryset = queryset.filter(is_event=is_event)

        # Filter by is_unmarried if provided
        if is_unmarried is not None:
            queryset = queryset.filter(is_unmarried=is_unmarried)

        # Filter by is_pet if provided
        if is_pet is not None:
            queryset = queryset.filter(is_pet=is_pet)


        return queryset


    def create(self, request, *args, **kwargs):
        # Get the room_number and property_id from the request data
        room_number = request.data.get('room_number')
        property_id = request.data.get('property')

        # Check if the room_number already exists for the given property
        existing_room = hotel_models.Room.objects.filter(room_number=room_number, property_id=property_id)
        print('Existing room check:', existing_room.exists())

        if existing_room.exists():
            return Response(
                {"room_number": ["Room with this room number already exists for this property."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        # If it doesn't exist, call the super class's create method
        return super().create(request, *args, **kwargs)


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


# API to list and create messages without requiring authentication
class ContactMessageListCreateView(generics.ListCreateAPIView):
    serializer_class = hotel_serializers.ContactMessageSerializer

    def get_queryset(self):
        # For anonymous users, we'll need to ensure that no authentication is required
        return hotel_models.ContactMessage.objects.all().order_by('-created_date')

    def perform_create(self, serializer):

        serializer.save()


# View for Guest Review
class ReviewListCreateAPIView(generics.ListCreateAPIView):
    queryset = hotel_models.Review.objects.all()
    serializer_class = hotel_serializers.ReviewSerializer

