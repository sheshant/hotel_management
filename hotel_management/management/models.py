import os

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

# Create your models here.
from management.constants import GENDER, ROOM_TYPES, STATUS, BOOKING_STATUS


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    photo_path = models.ImageField(upload_to='images/', default=os.path.join(settings.BASE_DIR, 'images/xrSh9Z0.jpg'))
    gender = models.CharField(max_length=15, choices=GENDER)

    def __str__(self):
        return self.user.get_full_name()


class Address(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    street = models.CharField(max_length=100, blank=True)
    landmark = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = ('city', 'state', 'pincode', 'street', 'landmark', )

    def __str__(self):
        return 'city: {} state: {} pincode: {} street: {} landmark: {} '.format(
            self.city, self.state, self.pincode, self.street, self.landmark)


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    address = models.OneToOneField(Address, related_name='hotel')
    contact_number = models.CharField(max_length=12)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} {}'.format(self.name, self.address.city)


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='rooms')
    user = models.OneToOneField(User, related_name='room', default=None, null=True, blank=True)
    type = models.CharField(max_length=20, choices=ROOM_TYPES)
    status = models.CharField(max_length=20, choices=STATUS)
    price = models.IntegerField(default=0)
    room_no = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('hotel', 'room_no', )

    def __str__(self):
        return self.room_no


class Booking(models.Model):
    user = models.ForeignKey(User, related_name='user_bookings')
    room = models.ForeignKey(Room, related_name='room')
    hotel = models.ForeignKey(Hotel, related_name='hotel')
    status = models.CharField(max_length=20, choices=BOOKING_STATUS, default='not_cancelled')
    date_of_booking = models.DateTimeField(auto_now_add=True)
    date_of_stay = models.DateTimeField()
    last_date_of_stay = models.DateTimeField()

