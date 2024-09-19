from rest_framework import generics
# from rest_framework.parsers import MultiPartParser, FormParser
# from .models import Property
from hotel import models as hotel_models
# from .serializers import PropertySerializer
from hotel import serializers as hotel_serializers



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

# Retrieve, Update, and Delete a specific property
class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = hotel_models.Property.objects.all()
    serializer_class = hotel_serializers.PropertySerializer
    # parser_classes = [MultiPartParser, FormParser]

    # def put(self, request, *args, **kwargs):
    #     print(request.data) 
    #     print(request.FILES)
    #     return super().put(request, *args, **kwargs)


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