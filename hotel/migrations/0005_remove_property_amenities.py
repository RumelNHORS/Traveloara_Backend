# Generated by Django 4.2.16 on 2024-09-26 09:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0004_property_amenities_room_description_room_map_url_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='amenities',
        ),
    ]
