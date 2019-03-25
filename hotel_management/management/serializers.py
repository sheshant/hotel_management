from rest_framework import serializers

from management.models import Hotel, Room, Booking


class HotelSerializer(serializers.ModelSerializer):
    city = serializers.SerializerMethodField(read_only=True)
    state = serializers.SerializerMethodField(read_only=True)
    pincode = serializers.SerializerMethodField(read_only=True)
    street = serializers.SerializerMethodField(read_only=True)
    landmark = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Hotel
        fields = [
            'id',
            'name',
            'city',
            'state',
            'pincode',
            'street',
            'landmark',
        ]

    def get_city(self, obj):
        return obj.address.city

    def get_state(self, obj):
        return obj.address.state

    def get_pincode(self, obj):
        return obj.address.pincode

    def get_street(self, obj):
        return obj.address.street

    def get_landmark(self, obj):
        return obj.address.landmark


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        exclude = ('user', 'created_at')


class BookingSerializer(serializers.ModelSerializer):
    number_of_days = serializers.SerializerMethodField(read_only=True)
    user_id = serializers.IntegerField(required=True)
    room_id = serializers.IntegerField(required=True)
    hotel_id = serializers.IntegerField(required=True)

    class Meta:
        model = Booking
        fields = ['user_id', 'room_id', 'hotel_id', 'date_of_booking', 'status', 'date_of_stay', 'last_date_of_stay',
                  'number_of_days']

    def get_number_of_days(self, obj):
        return (obj.last_date_of_stay - obj.date_of_stay).days


