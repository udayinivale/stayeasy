class HotelException(Exception):
    pass

class InvalidGuestError(HotelException):
    pass

class InvalidBookingError(HotelException):
    pass

class RoomNotAvailableError(HotelException):
    pass

class BookingNotFoundError(HotelException):
    pass

class InvalidBookingStatusError(HotelException):
    pass
