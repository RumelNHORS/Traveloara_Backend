from django.db import models
from django.utils import timezone
from django.conf import settings


# Choices for hotel status
PROPERTY_STATUS = (
    ("Draft", "Draft"),
    ("Disabled", "Disabled"),
    ("Rejected", "Rejected"),
    ("In Review", "In Review"),
    ("Live", "Live"),
)


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
    # amenities = models.CharField(max_length=255, blank=True, help_text="Comma separated amenities, e.g., Wi-Fi, Parking, Pool")
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
    map_url = models.URLField(max_length=200, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    # Adding room images
    image1 = models.ImageField(upload_to='rooms/', blank=True, null=True)
    image2 = models.ImageField(upload_to='rooms/', blank=True, null=True)
    image3 = models.ImageField(upload_to='rooms/', blank=True, null=True)
    image4 = models.ImageField(upload_to='rooms/', blank=True, null=True)
    image5 = models.ImageField(upload_to='rooms/', blank=True, null=True)

    def __str__(self):
        return f'{self.room_type} - Room No. {self.room_number}'
    

class RoomAmenities(models.Model):
    property = models.ForeignKey('Property', on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='amenities')
    amenity_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.amenity_name} (Property: {self.property}, Room: {self.room})"