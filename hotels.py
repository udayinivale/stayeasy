from models import Room,Standardroom,Deluxeroom,Suiteroom,Guest,Booking
from database import create_tables,load_rooms,add_guest,add_bookings,check_availability
import re

create_tables()
valid_data=load_rooms()
# print(valid_data)

def guest_registration():
    try:
        while True:
            name=input("enter the guest_name:").lower().strip()
            if name=="":
                print("name cannot be empty")
                continue
            break
    except Exception as e:
        print(e)

    try:
        while True:
            mobile_num=input("enter mobile number:")
            if mobile_num[0] not in ["6","7","8","9"]:
                print("invalid mobile number")
                continue
            break
    except Exception as e:
        print(e)

    try:
        while True:
            email=input("enter email id:")
            if not re.match(r"^[a-zA-Z0-9.]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}$",email):
                print("invalid email")
                continue
            if email=="":
                print("email cannot be empty.")
                continue
            break
    except Exception as e:
        print(e)

    try:
        while True:
            guest_count=int(input("enter number of guests:"))
            if guest_count<=0:
                print("guest count cannot be negative")
                continue
            break
    except Exception as e:
        print(e)

    guest_obj=Guest(name,email,mobile_num,guest_count)
    add_guest(name,mobile_num,email)
    return guest_obj
def rooms_available(room_type,check_in,check_out):
    occupied_rooms=check_availability(room_type,check_in,check_out)
    available_rooms=[]
    for room in room_obj:
        if room.room_type==room_type and (room.room_no,) not in occupied_rooms:
            available_rooms.append(room)
    return available_rooms


def create_booking():
    guest_obj=guest_registration()
    check_in=input("Enter check-in date:")
    check_out=input("Enter check-out date:")
    room_type=input("enter room type:").lower().strip()

    if room_type not in ["standard","deluxe","suite"]:
        print("invalid room type")
        return
    breakfast_choice="no"
    if room_type=="standard":
        breakfast_choice=input("Do you want breakfast? (yes/no):").lower().strip()
    guest_count=guest_obj.get_guest_count()
    max_guests={"standard":2,"deluxe":3,"suite":4}

    if guest_count>max_guests[room_type]:
        print("Maximum guests allowed:",max_guests[room_type])
        print("This room cannot accommodate",guest_count,"guests")
        print("\nAvailable room types:")

        for key,value in max_guests.items():
                count=0
                for room in room_obj:
                    if room.room_type==key:
                        count+=1
                if count>0:
                    print(key,"-",count,"rooms (Maximum",value,"guests)")

        print("Please register again with a suitable room type.")
        return

    occupied_rooms=check_availability(room_type,check_in,check_out)
    available_rooms=rooms_available(room_type,check_in,check_out)

    if not available_rooms:
        print("No rooms available for",room_type)
        print("\nOther available room types:")

        for key,value in max_guests.items():
            if key!=room_type and guest_count<=value:
                count=0
                for room in room_obj:
                    if room.room_type==key and (room.room_no,) not in occupied_rooms:
                        count+=1
                if count>0:
                    print(key,"-",count,"rooms (Maximum",value,"guests)")

        print("Please register again.")
        return

    selected_room=available_rooms[0]
    for room in available_rooms:
        if room.room_no<selected_room.room_no:
            selected_room=room

    try:
        booking_obj=Booking(guest_obj,selected_room,check_in,check_out,breakfast_choice)
        booking_id=add_bookings(
        guest_obj.get_mobile_num(),
        selected_room.room_no,
        check_in,
        check_out,
        guest_obj.get_guest_count(),
        booking_obj.get_total_amount()
        )
        booking_obj.set_booking_id(booking_id)
    except ValueError as e:
        print(e)
        return

    print("\nBooking Details")
    print("Guest Name:",guest_obj.get_name())
    print("Mobile Number:",guest_obj.get_mobile_num())
    print("Email:",guest_obj.get_email())
    print("Guest Count:",guest_obj.get_guest_count())
    print("Room Number:",selected_room.room_no)
    print("Room Type:",selected_room.room_type)
    print("Floor:",selected_room.floor)
    print("Check-in:",booking_obj.get_check_in())
    print("Check-out:",booking_obj.get_check_out())
    print("Booking Status:",booking_obj.get_booking_status())
    print("Total Amount:",booking_obj.get_total_amount())

room_obj=[]
for room in valid_data:
    room_no=int(room['room_no'])
    room_type=(room['room_type']).lower().strip()
    floor=int(room['floor'])
    if room_type=="standard":
        obj=Standardroom(room_no,room_type,floor)
    elif room_type=="deluxe":
        obj=Deluxeroom(room_no,room_type,floor)
    else:
        obj=Suiteroom(room_no,room_type,floor)
    room_obj.append(obj)

def search_availability():
    check_in=input("Enter check-in date:")
    check_out=input("Enter check-out date:")
    room_type=input("Enter room type:").lower().strip()

    if room_type not in ["standard","deluxe","suite"]:
        print("Invalid room type")
        return
    available_rooms=rooms_available(room_type,check_in,check_out)
    if not available_rooms:
        print("No rooms available for",room_type)
        return

    max_guests={"standard":2,"deluxe":3,"suite":4}

    for room in available_rooms:
        print("Room No:",room.room_no)

    print("Total available rooms:",len(available_rooms))
    print("Maximum guests allowed:",max_guests[room_type])






   
                    
    
while True:
    print("""
            1.search availability
            2.create booking
            3.check in
            4.check out
            5.cancel booking
            6.view booking details
            7.guest stay history
            8.occupancy report
            9.revenue report
            10.export bookings
            11.exit
    """)
    choice=input("Enter your choice:")

    if choice=="1":
        search_availability()
    elif choice=="2":
        create_booking()
    elif choice=="3":
        pass
    elif choice=="4":
        pass
    elif choice=="5":
        pass
    elif choice=="6":
        pass
    elif choice=="7":
        pass
    elif choice=="8":
        pass
    elif choice=="9":
        pass
    elif choice=="10":
        pass
    elif choice=="11":
        print("Thank you!" \
              "visit again..")
        break
    else:
        print("Invalid choice")
    
