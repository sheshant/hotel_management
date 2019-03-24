

GENDER = (
    ('male', 'MALE'),
    ('female', 'FEMALE'),
)

STATUS = (
    ('vacant', 'VACANT'),
    ('occupied', 'OCCUPIED'),
)

ROOM_TYPES = (
    ('single_occupancy', 'SINGLE_OCCUPANCY'),
    ('double_occupancy', 'DOUBLE_OCCUPANCY'),
    ('tripple_occupancy', 'TRIPPLE_OCCUPANCY'),
)

BOOKING_STATUS = (
    ('cancelled', 'CANCELLED'),
    ('not_cancelled', 'NOT_CANCELLED'),
)

ERROR_MESSAGES = {
    'INVALID_FIELDS': 'following fields are invalid {}',
    'INVALID_ORDER': 'ony 0 and 1 are allowed orders. Following are invalid {}',
    'MISSING_PARAMS': 'following necessary_params are missing {}',
    'ROOM_ALREADY_BOOKED': 'the room for booking is already booked',
    'BOOKING_ALREADY_CANCELLED': 'the booking id {} is already cancelled',
    'INVALID_BOOKING_ID': 'the booking id {} is not found',
    'NO_BOOKING_ID': 'necessary field booking_id not provided',
    'OCCUPIED_ROOM': 'Room id {} is already occupied with user id {}',
    'VACANT_ROOM': 'Room id {} is already vacant',
    'HOTEL_ROOM_MISMATCH': 'Room id {} is not in hotel id {}',
    'INVALID_DATE': "date of search cannot be less than current date",
    'INVALID_BOOKING_DATES': "date of stay {} cannot be less than last date of stay {}",
    'INVALID_ID': "{} ID {} not found",
    'BOOKING_IS_CANCELLED': 'the booking id {} is cancelled. No checkin/checkout',
    'INVALID_DATETIME_FORMAT': "the datetime format for date of stay or last date of stay is invalid. Desired format {}",
}

SUCCESS_MESSAGE = {
    'CANCEL_BOOKING': 'Booking id {} cancelled',
    'SUCCESSFULLY_CHECKED_IN': 'Booking id {} successfully checked in',
    'SUCCESSFULLY_CHECKED_OUT': 'Booking id {} successfully checked out',
}

