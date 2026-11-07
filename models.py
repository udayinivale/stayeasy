from abc import ABC,abstractmethod
from datetime import datetime,date
from pricing import calculate_total_amount

class Room(ABC):
    def __init__(self,room_no,room_type,floor):
        self.room_no=room_no
        self.room_type=room_type
        self.floor=floor
    @abstractmethod
    def tariff(self):
        pass

    @abstractmethod
    def extra_guest_charges(self,guest_count):
        pass

    @abstractmethod
    def breakfast(self,guest_count):
        pass
    
class Standardroom(Room):
    def __init__(self,room_no,room_type,floor):
        super().__init__(room_no,room_type,floor)
        self.base_price=2500
    
    def tariff(self):
        return self.base_price
    def extra_guest_charges(self,guest_count):
        return 0
    def breakfast(self,guest_count,choice):
        if choice=="yes":
         return guest_count*350
        return 0
    
    
class Deluxeroom(Room):
    def __init__(self,room_no,room_type,floor):
        super().__init__(room_no,room_type,floor)
        self.base_price=4000
   
    def tariff(self):
        return self.base_price
    def extra_guest_charges(self,guest_count):
        if guest_count>2:
            return (guest_count-2)*800
        return 0
    def breakfast(self,guest_count):
        return 0

class Suiteroom(Room):
    def __init__(self,room_no,room_type,floor):
        super().__init__(room_no,room_type,floor)
        self.base_price=7500
    
    def tariff(self):
        return self.base_price
    def extra_guest_charges(self,guest_count):
        if guest_count>2:
            return(guest_count-2)*800
        return 0
    def breakfast(self,guest_count):
        return 0

class Guest:
    def __init__(self,name,email,mobile_num,guest_count):
        self.set_name(name)
        self.set_email(email)
        self.set_mobile_num(mobile_num)
        self.set_guest_count(guest_count)

    def set_name(self,name):
        self.__name=name
    def get_name(self):
        return self.__name

    def set_email(self,email):
        if not email.strip():
            raise ValueError("Email cannot be empty")
        self.__email=email.strip()
    def get_email(self):
        return self.__email

    def set_mobile_num(self,mobile_num):
        if len(mobile_num)!=10:
            raise ValueError("invalid mobile number.")
        self.__mobile_num=mobile_num
    def get_mobile_num(self):
        return self.__mobile_num

    def set_guest_count(self,guest_count):
        self.__guest_count=guest_count
    def get_guest_count(self):
        return self.__guest_count

class Booking:
    def __init__(self,guest,room,check_in,check_out,breakfast_choice="no",completed_stays=0):
        self.set_guest(guest)
        self.set_room(room)
        self.set_check_in(check_in)
        self.set_check_out(check_out)
        self.__booking_status="confirmed"
        self.__total_amount=0
        self.__completed_stays=completed_stays
        self.calculate_total_amount(breakfast_choice)
        

    def set_booking_id(self,booking_id):
        self.__booking_id=booking_id
    def get_booking_id(self):
        return self.__booking_id
    
    def set_guest(self,guest):
        if not isinstance(guest,Guest):
            raise ValueError("invalid guest details")
        self.__guest=guest
    def get_guest(self):
        return self.__guest
    
    def set_room(self,room):
        if not isinstance(room,Room):
            raise ValueError("invalid room details")
        self.__room=room
    def get_room(self):
        return self.__room
    
    def set_check_in(self,check_in):
        check_in=datetime.strptime(check_in,"%d-%m-%Y").date()
        if check_in<date.today():
            raise ValueError("check-in date cannot be in the past")
        if (check_in-date.today()).days>180:
            raise ValueError("check-in date cannot be more than 180 days")
        self.__check_in=check_in
    def get_check_in(self):
        return self.__check_in
    
    def set_check_out(self,check_out):
        check_out=datetime.strptime(check_out,"%d-%m-%Y").date()
        if check_out<=self.__check_in:
            raise ValueError("check-out cannot be before check-in")
        if (check_out-self.__check_in).days>30:
            raise ValueError("The stay cannot exceed 30 nights")
        self.__check_out=check_out
    def get_check_out(self):
        return self.__check_out

    def set_booking_status(self,booking_status):
        booking_status=booking_status.lower()
        if self.__booking_status=="confirmed":
            if booking_status not in ("checked_in","cancelled"):
                raise ValueError("invalid status change")
        elif self.__booking_status=="checked_in":
            if booking_status!="checked_out":
                raise ValueError("invalid status change")
        else:
            raise ValueError("booking status cannot be changed")
        self.__booking_status=booking_status
    def get_booking_status(self):
        return self.__booking_status

    def set_total_amount(self,total_amount):
        if total_amount<0:
            raise ValueError("total amount cannot be negative")
        self.__total_amount=total_amount
    def get_total_amount(self):
        return self.__total_amount
    def calculate_total_amount(self,breakfast_choice):
        guest_count=self.__guest.get_guest_count()
        total=calculate_total_amount(self.__room,guest_count,self.__check_in,self.__check_out,breakfast_choice,self.__completed_stays)
        self.set_total_amount(total)
    
    def __str__(self):
        return f"Booking ID: {self.__booking_id}, Status: {self.__booking_status}, Total Amount: {self.__total_amount}"
    
    
    
