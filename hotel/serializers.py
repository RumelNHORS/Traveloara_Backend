# serializers.py
from rest_framework import serializers
from hotel import models as hotel_models
import re


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


# Contact With Host Serializer
class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = hotel_models.ContactMessage
        fields = ['id', 'sender', 'recipient', 'message', 'created_date']

    def to_representation(self, instance):
        """Override to customize how the message is serialized."""
        representation = super().to_representation(instance)
        # Hide phone numbers and email addresses in the message
        representation['message'] = self.hide_contact_info(representation['message'])
        return representation
    
    def hide_contact_info(self, message):
        """Hide phone numbers and email addresses."""
        # Regex for phone numbers (basic example, can be adjusted)
        phone_pattern = r'\b\d{10,15}\b'
        # Regex for email addresses
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

        # Replace phone numbers with '[HIDDEN]'
        message = re.sub(phone_pattern, '[HIDDEN]', message)
        # Replace email addresses with '[HIDDEN]'
        message = re.sub(email_pattern, '[HIDDEN]', message)

        return message
    
# This is for hiding the phone nmber including the spech(0 1 5 3 8 5 4 2 4 5)
# class ContactMessageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = hotel_models.ContactMessage
#         fields = ['sender', 'recipient', 'message', 'created_date']

#     def to_representation(self, instance):
#         """Override to customize how the message is serialized."""
#         representation = super().to_representation(instance)
#         # Hide phone numbers and email addresses in the message
#         representation['message'] = self.hide_contact_info(representation['message'])
#         return representation

#     def hide_contact_info(self, message):
#         """Hide phone numbers and email addresses."""
#         # Regex for phone numbers with optional spaces between digits
#         phone_pattern = r'\b(?:\d\s*){10,15}\b'
#         # Regex for email addresses with optional spaces between characters
#         email_pattern = r'(?:(?:[a-zA-Z0-9._%+-](?:\s*)?)+@(?:[a-zA-Z0-9.-]+(?:\s*)?\.[a-zA-Z]{2,})+)'
#         # Replace phone numbers with '[HIDDEN]'
#         message = re.sub(phone_pattern, '[HIDDEN]', message)
#         # Replace email addresses with '[HIDDEN]'
#         message = re.sub(email_pattern, '[HIDDEN]', message)

#         return message
# Serializer for the Guest Review


class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    room_type = serializers.SerializerMethodField()

    class Meta:
        model = hotel_models.Review
        fields = ['id', 'user', 'username', 'room', 'room_type', 'rating', 'message']
        read_only_fields = ['user']

    def get_username(self, obj):
        return obj.user.username

    def get_room_type(self, obj):
        return obj.room.room_type