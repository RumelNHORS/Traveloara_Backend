from django.contrib import admin
from hotel import models as hotel_models

# Register your models here.
admin.site.register(hotel_models.Property)
admin.site.register(hotel_models.Room)
