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
    formatted_amenities = serializers.SerializerMethodField()
    class Meta:
        model = hotel_models.Room
        fields = '__all__'

    def get_formatted_amenities(self, obj):
        # Ensure room_amenities is not empty
        amenities = obj.room_amenities
        if amenities:
            # Split the amenities on commas or any other delimiter
            amenities_list = [amenity.strip() for amenity in amenities.split(',')]
            print('################################')
            print('amenities_list:', amenities_list)
            print('################################')
            # Join the amenities with period and new line for formatting
            return '.\n'.join(amenities_list) + '.'
        return ''
        

class RoomAmenitiesSerializer(serializers.ModelSerializer):
    # property = PropertySerializer()
    # room = RoomSerializer()
    class Meta:
        model = hotel_models.RoomAmenities
        # fields = ['id', 'property', 'room', 'amenity_name']
        fields = '__all__'
        