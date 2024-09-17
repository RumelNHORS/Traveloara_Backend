from django.urls import path
# from .views import PropertyListCreateView, PropertyDetailView
from hotel import views as hotel_views



urlpatterns = [
    # For listing all properties or creating a new properties
    path('properties/', hotel_views.PropertyListCreateView.as_view(), name='property_list_create'),
    # For retrieving, updating, or deleting a specific properties
    path('properties/<int:pk>/', hotel_views.PropertyDetailView.as_view(), name='property_detail'),
    # For listing all rooms or creating a new room
    path('rooms/', hotel_views.RoomListCreateView.as_view(), name='room_list_create'),
    # For retrieving, updating, or deleting a specific room
    path('rooms/<int:pk>/', hotel_views.RoomDetailView.as_view(), name='room_detail'),
    # Creating the Room Amenities
    path('amenities/', hotel_views.RoomAmenitiesListCreateView.as_view(), name='amenities_list_create'),
    # Update, Delete Aminities
    path('amenities/<int:pk>/', hotel_views.RoomAmenitiesDetailView.as_view(), name='amenities_detail'),
]