# serializers.py
from rest_framework import serializers
from hotel import models as hotel_models



# Property Serializer
class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = hotel_models.Property
        fields = '__all__'

    def update(self, instance, validated_data):
        # If 'image' is not in validated_data, we retain the existing image
        image = validated_data.get('image', None)
        if image is None:
            # If no image provided, keep the current image
            validated_data['image'] = instance.image
        return super().update(instance, validated_data)


# Room Serializer
class RoomSerializer(serializers.ModelSerializer):
    # Add a custom field to display the address of the property
    property_address = serializers.CharField(source='property.address', read_only=True)
    # Custom field to display the user id of the property's owner
    user_id = serializers.IntegerField(source='property.user.id', read_only=True)
    class Meta:
        model = hotel_models.Room
        fields = '__all__'
        # Add 'property_address' as a custom field
        extra_fields = ['property_address', 'user_id']
        

class RoomAmenitiesSerializer(serializers.ModelSerializer):
    # property = PropertySerializer()
    # room = RoomSerializer()
    class Meta:
        model = hotel_models.RoomAmenities
        # fields = ['id', 'property', 'room', 'amenity_name']
        fields = '__all__'


# Serializer for the Booking
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = hotel_models.Booking
        fields = '__all__'
        # fields = ['id', 'user', 'email', 'phone', 'property', 'room', 'checkin_date', 'checkout_date', 'num_adult', 'num_children', 'num_infants', 'payment_id']   