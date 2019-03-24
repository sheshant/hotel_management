from django.conf.urls import url

from management.views import SearchHotel, SearchRoom, BookRoom, CancelBooking, Checkout, Checkin, GetAllBookings

urlpatterns = [
    url(r'^search_hotel/$', SearchHotel.as_view(), name='search_hotel'),
    url(r'^search_room/$', SearchRoom.as_view(), name='search_room'),
    url(r'^book_room/$', BookRoom.as_view(), name='book_room'),
    url(r'^cancel_booking/$', CancelBooking.as_view(), name='cancel_booking'),
    url(r'^checkout/$', Checkout.as_view(), name='checkout'),
    url(r'^checkin/$', Checkin.as_view(), name='checkin'),
    url(r'^get_all_bookings/$', GetAllBookings.as_view(), name='get_all_bookings'),
]
