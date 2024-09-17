# serializers.py
from rest_framework import serializers
from hotel import models as hotel_models



# Property Serializer
class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = hotel_models.Property
        fields = '__all__'


# Room Serializer
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = hotel_models.Room
        fields = '__all__'