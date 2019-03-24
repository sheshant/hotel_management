from datetime import datetime

from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED

from management.constants import ERROR_MESSAGES, SUCCESS_MESSAGE
from management.models import Hotel, Room, Booking
from management.serializers import HotelSerializer, RoomSerializer, BookingSerializer


def check_database(id, model):
    if not model.objects.filter(pk=id).exists():
        return Response(data={'error': ERROR_MESSAGES['INVALID_ID'].format(model.__name__, id)},
                        status=HTTP_400_BAD_REQUEST)
    return id


def search_hotel(request, paginator):
    """

    :param request:
    :param paginator:
    :return:
    """
    params = request.data
    city = params.get('city')
    state = params.get('state')
    pincode = params.get('pincode')

    queryset = Hotel.objects.all().prefetch_related('address').order_by('-created_at')

    if city:
        queryset = queryset.filter(address__city=city)
    if state:
        queryset = queryset.filter(address__state=state)
    if pincode:
        queryset = queryset.filter(address__pincode=pincode)

    page = paginator.paginate_queryset(queryset, request)
    hotel_serializer = HotelSerializer(page, many=True)
    return paginator.get_paginated_response(hotel_serializer.data)


def search_room(request, paginator):
    params = request.data
    hotel_id = params.get('hotel_id')
    upper_price = params.get('upper_price')
    lower_price = params.get('lower_price')
    type = params.get('type')

    queryset = Room.objects.filter(user=None, status='vacant')
    if hotel_id:
        queryset = queryset.filter(hotel_id=hotel_id)
    if upper_price:
        queryset = queryset.filter(price__lte=upper_price)
    if lower_price:
        queryset = queryset.filter(price__gte=lower_price)
    if type:
        queryset = queryset.filter(type=type)
    queryset = queryset.order_by('-created_at')

    page = paginator.paginate_queryset(queryset, request)
    room_serializer = RoomSerializer(page, many=True)
    return paginator.get_paginated_response(room_serializer.data)


def show_bookings(request, paginator):
    params = request.data
    hotel_id = params.get('hotel_id')
    user_id = params.get('user_id')
    room_id = params.get('room_id')
    status = params.get('status')
    date_of_booking = params.get('date_of_booking')
    date_of_stay = params.get('date_of_stay')
    sort_by = params.get('sort_by', [])

    sort_by_fields = []
    sort_by_order = []
    for record in sort_by:
        sort_by_fields.append(record.get('field', ''))
        sort_by_order.append(record.get('order', ''))

    booking_fields = [field.attname for field in Booking._meta.fields]
    invalid_fields = [field for field in sort_by_fields if field not in booking_fields]
    if invalid_fields:
        return Response(data=ERROR_MESSAGES['INVALID_FIELDS'].format(', '.join(invalid_fields)),
                        status=HTTP_400_BAD_REQUEST)

    invalid_orders = set(sort_by_order).difference(set({'1', '0'}))
    if invalid_orders:
        return Response(data=ERROR_MESSAGES['INVALID_ORDER'].format(', '.join(invalid_orders)),
                        status=HTTP_400_BAD_REQUEST)

    sort_by_params = []
    for record in sort_by:
        order = record.get('order', '')
        sort_by_params.append('{}{}'.format('' if order == '0' else '-', record.get('field', '')))

    queryset = Booking.objects.all()
    if hotel_id:
        queryset = queryset.filter(hotel_id=hotel_id)
    if user_id:
        queryset = queryset.filter(user_id=user_id)
    if room_id:
        queryset = queryset.filter(room_id=room_id)
    if status:
        queryset = queryset.filter(status=status)
    if date_of_booking:
        queryset = queryset.filter(date_of_booking=date_of_booking)
    if date_of_stay:
        queryset = queryset.filter(date_of_stay=date_of_stay)
    queryset = queryset.order_by(*sort_by_params)

    page = paginator.paginate_queryset(queryset, request)
    room_serializer = RoomSerializer(page, many=True)
    return paginator.get_paginated_response(room_serializer.data)


def book_room(params):
    important_params = ['hotel_id', 'user_id', 'room_id', 'date_of_stay', 'last_date_of_stay']
    missing_params = [param for param in important_params if not params.get(param)]
    if missing_params:
        return Response(data={'error': ERROR_MESSAGES['MISSING_PARAMS'].format(', '.join(missing_params))},
                        status=HTTP_400_BAD_REQUEST)

    hotel_id = check_database(params.get('hotel_id'), Hotel)
    if isinstance(hotel_id, Response):
        return hotel_id

    user_id = check_database(params.get('user_id'), User)
    if isinstance(user_id, Response):
        return user_id

    room_id = check_database(params.get('room_id'), Room)
    if isinstance(room_id, Response):
        return room_id

    if not Room.objects.filter(id=room_id, hotel_id=hotel_id).exists():
        return Response(data={'error': ERROR_MESSAGES['HOTEL_ROOM_MISMATCH'].format(room_id, hotel_id)},
                        status=HTTP_400_BAD_REQUEST)

    try:
        last_date_of_stay = datetime.strptime(params.get('last_date_of_stay'), "%Y-%m-%d %H:%M:%S")
        if last_date_of_stay < datetime.now():
            return Response(data={'error': ERROR_MESSAGES['INVALID_DATE']}, status=HTTP_400_BAD_REQUEST)

        date_of_stay = datetime.strptime(params.get('date_of_stay'), "%Y-%m-%d %H:%M:%S")
        if date_of_stay < datetime.now():
            return Response(data={'error': ERROR_MESSAGES['INVALID_DATE']}, status=HTTP_400_BAD_REQUEST)

        if date_of_stay >= last_date_of_stay:
            return Response(data={'error': ERROR_MESSAGES['INVALID_BOOKING_DATES'].format(
                date_of_stay, last_date_of_stay)}, status=HTTP_400_BAD_REQUEST)

    except ValueError:
        return Response(data={'error': ERROR_MESSAGES['INVALID_DATETIME_FORMAT'].format('YYYY-MM-DD HH:MM:SS')},
                        status=HTTP_400_BAD_REQUEST)

    bookings = Booking.objects.filter(Q(date_of_stay__lte=date_of_stay, last_date_of_stay__gte=date_of_stay) |
                                      Q(date_of_stay__gte=date_of_stay, last_date_of_stay__lte=last_date_of_stay) |
                                      Q(date_of_stay__lte=last_date_of_stay,
                                        last_date_of_stay__gte=last_date_of_stay)).filter(
        room_id=room_id, status='not_cancelled')
    if bookings.exists():
        return Response(data={'error': ERROR_MESSAGES['ROOM_ALREADY_BOOKED']}, status=HTTP_400_BAD_REQUEST)

    data_params = {
        'user_id': user_id, 'hotel_id': hotel_id, 'room_id': room_id, 'date_of_stay': date_of_stay,
        'last_date_of_stay': last_date_of_stay,
    }

    booking_serializer = BookingSerializer(data=data_params)
    if booking_serializer.is_valid():
        booking_serializer.save()
        return Response(data=booking_serializer.data, status=HTTP_201_CREATED)
    else:
        return Response(data=booking_serializer.errors, status=HTTP_400_BAD_REQUEST)


def cancel_booking(params):
    booking_id = params.get('booking_id')
    if booking_id:
        booking = Booking.objects.filter(pk=booking_id).first()
        if booking:
            if booking.status == 'not_cancelled':
                booking.status = 'cancelled'
                booking.save()
                return Response(data={'message': SUCCESS_MESSAGE['CANCEL_BOOKING'].format(booking_id)},
                                status=HTTP_200_OK)
            else:
                return Response(data={'error': ERROR_MESSAGES['BOOKING_ALREADY_CANCELLED'].format(booking.pk)},
                                status=HTTP_400_BAD_REQUEST)

        else:
            return Response(data={'error': ERROR_MESSAGES['INVALID_BOOKING_ID'].format(booking_id)},
                            status=HTTP_400_BAD_REQUEST)
    else:
        return Response(data={'error': ERROR_MESSAGES['NO_BOOKING_ID']}, status=HTTP_400_BAD_REQUEST)


def checkin(params):
    booking_id = params.get('booking_id')
    if booking_id:
        booking = Booking.objects.filter(pk=booking_id).first()
        if booking:
            if booking.status == 'cancelled':
                return Response(data={'error': ERROR_MESSAGES['BOOKING_IS_CANCELLED'].format(booking.pk)},
                                status=HTTP_400_BAD_REQUEST)

            room = booking.room
            if room.user:
                return Response(data={'error': ERROR_MESSAGES['OCCUPIED_ROOM'].format(room.pk, room.user.pk)},
                                status=HTTP_400_BAD_REQUEST)
            else:
                room.status = 'occupied'
                room.user = booking.user
                room.save()
                return Response(data={'message': SUCCESS_MESSAGE['SUCCESSFULLY_CHECKED_IN'].format(booking_id)},
                                status=HTTP_200_OK)
        else:
            return Response(data={'error': ERROR_MESSAGES['INVALID_BOOKING_ID'].format(booking_id)},
                            status=HTTP_400_BAD_REQUEST)
    else:
        return Response(data={'error': ERROR_MESSAGES['NO_BOOKING_ID']}, status=HTTP_400_BAD_REQUEST)


def checkout(params):
    booking_id = params.get('booking_id')
    if booking_id:
        booking = Booking.objects.filter(pk=booking_id).first()
        if booking:
            if booking.status == 'cancelled':
                return Response(data={'error': ERROR_MESSAGES['BOOKING_IS_CANCELLED'].format(booking.pk)},
                                status=HTTP_400_BAD_REQUEST)

            room = booking.room
            if not room.user:
                return Response(data={'error': ERROR_MESSAGES['VACANT_ROOM'].format(room.pk)},
                                status=HTTP_400_BAD_REQUEST)
            else:
                room.status = 'vacant'
                room.user = None
                room.save()
                return Response(data={'message': SUCCESS_MESSAGE['SUCCESSFULLY_CHECKED_OUT'].format(booking_id)},
                                status=HTTP_200_OK)

        else:
            return Response(data={'error': ERROR_MESSAGES['INVALID_BOOKING_ID'].format(booking_id)},
                            status=HTTP_400_BAD_REQUEST)
    else:
        return Response(data={'error': ERROR_MESSAGES['NO_BOOKING_ID']}, status=HTTP_400_BAD_REQUEST)

