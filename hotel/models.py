from django.db import models
from django.utils import timezone
from django.conf import settings
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

# Choices for hotel status
PROPERTY_STATUS = (
    ("Draft", "Draft"),
    ("Disabled", "Disabled"),
    ("Rejected", "Rejected"),
    ("In Review", "In Review"),
    ("Live", "Live"),
)
# Payment Status Choices
PAYMENT_STATUS = (
    ('Pending', 'Pending'),
    ('Completed', 'Completed'),
    ('Failed', 'Failed'),
)
# Cancelation policy Choice
CANCELATION_CHOICE = (
    ('Non Refundable', 'Non Refundable'),
    ('Flexible', 'Flexible'),
    ('Moderate', 'Moderate'),
)

# Lease type choices for properties (office spaces)
LEASE_TYPE_CHOICES = [
    ('hourly', 'Hourly'),
    ('daily', 'Daily'),
    ('weekly', 'Weekly'),
    ('monthly', 'Monthly'),
    ('yearly', 'Yearly'),
]

PROPERTY_TYPE_CHOICES = [
    ('room', 'Room'),
    ('hotel', 'Hotel'),
    ('resort', 'Resort'),
    ('office', 'Office Space'),
    ('apartment', 'Apartment'),
    ('hotel_apartment', 'Hotel Apartment'),
    ('pg', 'Paying Guest'),
    ('store', 'Store'),
]

# Models For Adding Property
class Property(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    property_name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='properties/')
    address = models.CharField(max_length=255)
    mobile = models.CharField(max_length=20)
    email = models.EmailField()
    # city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    city = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=PROPERTY_STATUS, default='Live')
    # New field for comma-separated amenities
    amenities = models.TextField(blank=True, null=True)
    
    # New field for property type
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES, default='Room')

    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.property_name
    

# Room Models for Property
class Room(models.Model):
    property = models.ForeignKey('Property', on_delete=models.CASCADE)
    # e.g., Single, Double, Suite, etc.
    room_type = models.CharField(max_length=255)
    room_number = models.CharField(max_length=10)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_beds = models.PositiveIntegerField()
    room_capacity = models.PositiveIntegerField()
    number_of_bedrooms = models.PositiveIntegerField()
    number_of_bathrooms = models.PositiveIntegerField()
    description = models.TextField()
    # map_url = models.URLField(max_length=200, blank=True, null=True)
    map_url = models.TextField()
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    # Adding room images
    image1 = models.ImageField(upload_to='rooms/', blank=True, null=True)
    image2 = models.ImageField(upload_to='rooms/', blank=True, null=True)
    image3 = models.ImageField(upload_to='rooms/', blank=True, null=True)
    image4 = models.ImageField(upload_to='rooms/', blank=True, null=True)
    image5 = models.ImageField(upload_to='rooms/', blank=True, null=True)
    # Adding room amenities
    room_amenities = models.TextField(null=True, blank=True)

    is_smoking = models.BooleanField(default=False)
    is_media = models.BooleanField(default=False)
    is_event = models.BooleanField(default=False)
    is_unmarried = models.BooleanField(default=False)
    is_pet = models.BooleanField(default=False)
    # Checkin and Check out
    check_in = models.TimeField(default=datetime.time(12, 0))
    check_out = models.TimeField(default=datetime.time(11, 0))
    # Cancelation Policy
    canceletion_policy = models.CharField(max_length=250, choices=CANCELATION_CHOICE, default='Flexible')
    def __str__(self):
        return f'{self.room_type} - Room No. {self.room_number}'


class RoomAmenities(models.Model):
    property = models.ForeignKey('Property', on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='amenities')
    amenity_name = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.amenity_name} (Property: {self.property}, Room: {self.room})"
    

class ContactMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages_sent')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages_received')
    message = models.TextField(help_text="Enter your message here")
    created_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username}"
    


# Model For Client Review
class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_review')
    room = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='room_review')
    message = models.TextField()
    # Assuming the rating scale is 1 to 5
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],help_text="Rate the room from 1 (worst) to 5 (best)")
    create_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Review from {self.user.username} to {self.room.room_type} - Rating: {self.rating}/5"