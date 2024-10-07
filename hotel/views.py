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

    # For Filter the Rooms by the User Id
    def get_queryset(self):
        # Get user_id from query parameters
        user_id = self.request.query_params.get('user_id', None)
        # Get property_id from the query parameters
        property_id = self.request.query_params.get('property_id', None)

        if user_id:
            # Filter rooms by the provided user_id from the Property model(GET /rooms/?user_id=11)
            return hotel_models.Room.objects.filter(property__user_id=user_id)
        
        # Filter rooms by property_id if provided (GET /rooms/?property_id=5)
        if property_id:
            return hotel_models.Room.objects.filter(property_id=property_id)
        
        # If no user_id is provided, return all rooms
        return hotel_models.Room.objects.all()


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


# View for Booking Rooms
# class BookingListCreateAPIView(generics.ListCreateAPIView):
#     queryset = hotel_models.Booking.objects.all()
#     serializer_class = hotel_serializers.BookingSerializer

#     def create(self, request, *args, **kwargs):
#         # Get the room and check its availability
#         room_id = request.data.get('room')
#         room = hotel_models.Room.objects.filter(id=room_id, is_available=True).first()

#         if not room:
#             return Response(
#                 {"room": ["Room is not available for booking."]},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Parse the checkin and checkout dates
#         checkin_date = parse_date(request.data.get('checkin_date'))
#         checkout_date = parse_date(request.data.get('checkout_date'))

#         if not checkin_date or not checkout_date:
#             return Response(
#                 {"dates": ["Invalid date format. Use YYYY-MM-DD."]},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         if checkin_date >= checkout_date:
#             return Response(
#                 {"dates": ["Checkout date must be after the checkin date."]},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Calculate total_days based on checkin and checkout dates
#         total_days = (checkout_date - checkin_date).days
#         if total_days <= 0:
#             return Response(
#                 {"dates": ["Total days must be at least 1."]},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Calculate the total price and should_pay
#         per_night = room.price_per_night
#         total_amount = per_night * total_days

#         # Ensure the payment_status is a valid string, not a list
#         payment_status = request.data.get('payment_status', 'Pending')
#         if isinstance(payment_status, list):
#             payment_status = payment_status[0]


#         # Calculate total guests
#         num_adult = int(request.data.get('num_adult', 1))
#         num_children = int(request.data.get('num_children', 0))
#         num_infants = int(request.data.get('num_infants', 0))
#         total_guests = num_adult + num_children + num_infants
#         print('#########################################')
#         print('Total Guests:', total_guests)
#         print('#########################################')
        

#         # Ensure fields have the correct types (e.g., primary keys, decimal fields)
#         try:
#             booking_data = {
#                 "user": request.data.get('user'),
#                 "payment_status": payment_status,
#                 "email": request.data.get('email'),
#                 "phone": request.data.get('phone'),
#                 "property": request.data.get('property'),
#                 "room": request.data.get('room'),
#                 "before_discount": request.data.get('before_discount', None),
#                 "per_night": per_night,
#                 "saved": request.data.get('saved', None),
#                 "checkin_date": checkin_date,
#                 "checkout_date": checkout_date,
#                 "total_days": total_days,
#                 "num_adult": int(request.data.get('num_adult', 1)),
#                 "num_children": int(request.data.get('num_children', 0)),
#                 "num_infants": int(request.data.get('num_infants', 0)),
#                 "total_guests": total_guests,
#                 "payment_id": request.data.get('payment_id'),
#                 "total_amount": total_amount,
#                 "created_date": request.data.get('created_date', timezone.now()),
#             }
#         except ValueError as e:
#             raise ValidationError({"error": f"Invalid data type: {str(e)}"})

#         # Validate the serializer with the corrected data
#         serializer = self.get_serializer(data=booking_data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)

#         # Mark the room as unavailable (optional)
#         room.is_available = False
#         room.save()

#         return Response(serializer.data, status=status.HTTP_201_CREATED)


class BookingListCreateAPIView(generics.ListCreateAPIView):
    queryset = hotel_models.Booking.objects.all()
    serializer_class = hotel_serializers.BookingSerializer

    def create(self, request, *args, **kwargs):
        # Get the room and check its availability
        room_id = request.data.get('room')
        room = hotel_models.Room.objects.filter(id=room_id, is_available=True).first()

        if not room:
            return Response(
                {"room": ["Room is not available for booking."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Parse the checkin and checkout dates
        checkin_date = parse_date(request.data.get('checkin_date'))
        checkout_date = parse_date(request.data.get('checkout_date'))

        if not checkin_date or not checkout_date:
            return Response(
                {"dates": ["Invalid date format. Use YYYY-MM-DD."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        if checkin_date >= checkout_date:
            return Response(
                {"dates": ["Checkout date must be after the checkin date."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Calculate total_days based on checkin and checkout dates
        total_days = (checkout_date - checkin_date).days
        print('Total Days based on your checkin and checkout date:', total_days)
        if total_days <= 0:
            return Response(
                {"dates": ["Total days must be at least 1."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Calculate the total price and should_pay
        per_night = room.price_per_night
        total_amount = per_night * total_days
        print('Total Amount for this Room based on your total days:', total_amount)

        # Ensure the payment_status is a valid string, not a list
        payment_status = request.data.get('payment_status', 'Pending')
        if isinstance(payment_status, list):
            payment_status = payment_status[0]

        # Handle empty or invalid num_adult, num_children, num_infants values
        try:
            num_adult = int(request.data.get('num_adult', 1) or 1)
            num_children = int(request.data.get('num_children', 0) or 0)
            num_infants = int(request.data.get('num_infants', 0) or 0)
        except ValueError:
            return Response(
                {"guests": ["Invalid number of guests provided."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Calculate total guests
        # total_guests = num_adult + num_children + num_infants
        total_guests = num_adult + num_children
        print('Total Guest based on the Number of Adult and the number of Children:', total_guests)

        # Ensure fields have the correct types (e.g., primary keys, decimal fields)
        try:
            booking_data = {
                "user": request.data.get('user'),
                "payment_status": payment_status,
                "email": request.data.get('email'),
                "phone": request.data.get('phone'),
                "property": request.data.get('property'),
                "room": request.data.get('room'),
                "before_discount": request.data.get('before_discount', None),
                "per_night": per_night,
                "saved": request.data.get('saved', None),
                "checkin_date": checkin_date,
                "checkout_date": checkout_date,
                "total_days": total_days,
                "num_adult": num_adult,
                "num_children": num_children,
                "num_infants": num_infants,
                "total_guests": total_guests,
                "payment_id": request.data.get('payment_id'),
                "total_amount": total_amount,
                "created_date": request.data.get('created_date', timezone.now()),
            }
        except ValueError as e:
            raise ValidationError({"error": f"Invalid data type: {str(e)}"})

        # Validate the serializer with the corrected data
        serializer = self.get_serializer(data=booking_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Mark the room as unavailable (optional)
        room.is_available = False
        room.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

