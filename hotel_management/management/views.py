
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

from management.utils import search_hotel, search_room, show_bookings, book_room, cancel_booking, checkin, checkout


class SearchHotel(APIView):
    pagination_class = PageNumberPagination
    paginator = pagination_class()

    def post(self, request):
        return search_hotel(request, self.paginator)


class SearchRoom(APIView):
    pagination_class = PageNumberPagination
    paginator = pagination_class()

    def post(self, request):
        return search_room(request, self.paginator)


class GetAllBookings(APIView):
    pagination_class = PageNumberPagination
    paginator = pagination_class()

    def post(self, request):
        return show_bookings(request, self.paginator)


class BookRoom(APIView):

    def post(self, request):
        return book_room(request.data)


class CancelBooking(APIView):

    def post(self, request):
        return cancel_booking(request.data)


class Checkin(APIView):

    def post(self, request):
        return checkin(request.data)


class Checkout(APIView):

    def post(self, request):
        return checkout(request.data)


