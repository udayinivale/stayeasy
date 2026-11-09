from models import Room,Standardroom,Deluxeroom,Suiteroom,Guest,Booking
from database import create_tables,load_rooms,add_guest,add_bookings,check_availability,check_in_booking,check_out_booking,count_completed_stays,guest_stay_history,view_booking_details,cancel_booking,export_bookings
import re
from invoices import generate_invoice
from reports import occupancy_report,revenue_report

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
    completed_stays=count_completed_stays(guest_obj.get_mobile_num())
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
        booking_obj=Booking(guest_obj,selected_room,check_in,check_out,breakfast_choice,completed_stays)
        booking_id=add_bookings(
            guest_obj.get_mobile_num(),
            selected_room.room_no,
            check_in,
            check_out,
            guest_obj.get_guest_count(),
            booking_obj.get_total_amount(),
            breakfast_choice,
            completed_stays,
            booking_obj.get_room_revenue(),
            booking_obj.get_gst_amount()
        )
        booking_obj.set_booking_id(booking_id)
        
    except ValueError as e:
        print(e)
        return

    print("\nBooking successful.")
    

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

def check_in():
    booking_id=input("enter booking id:")
    result=check_in_booking(booking_id)
    print(result)

def check_out():
    booking_id=input("enter booking id:").strip().upper()
    result=check_out_booking(booking_id)
    print(result)

    if result=="checked-out successfully":
        generate_invoice(booking_id)
        print("Invoice generated successfully.")

def cancel_booking_room():
    booking_id=input("Enter booking ID:")
    result=cancel_booking(booking_id)

    if isinstance(result,tuple):
        refund,retained_amount=result
        print("Booking cancelled successfully")
        print("Refund Amount: Rs.",refund)
        print("Amount Retained: Rs.",retained_amount)
    else:
        print(result)

def view_guest_history():
    mobile_num=input("Enter mobile number:")
    result=guest_stay_history(mobile_num)

    if not result:
        print("No stay history found")
        return

    print("\nGuest Stay History")
    for row in result:
        print("Booking ID:",f"BK{row[0]:04d}")
        print("Room Number:",row[1])
        print("Check-in:",row[2])
        print("Check-out:",row[3])
        print("Status:",row[4])
        print("Total Amount:",row[5])
        
def view_booking():
    booking_id=input("Enter booking ID:")
    result=view_booking_details(booking_id)

    if result is None:
        print("Booking not found.")
    else:
        print("Booking ID:",f"BK{result[0]:04d}")
        print("Guest name:",result[1])
        print("Mobile number:",result[2])
        print("Email:",result[3])
        print("Room number:",result[4])
        print("Room type:",result[5])
        print("Check-in:",result[6])
        print("Check-out:",result[7])
        print("Guest count:",result[8])
        print("Booking status:",result[9])
        print("Total amount:",result[10])
                    
    
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
        check_in()
    elif choice=="4":
        check_out()
    elif choice=="5":
        cancel_booking_room()
    elif choice=="6":
        view_booking()
    elif choice=="7":
        view_guest_history()
    elif choice=="8":
        occupancy_report()
    elif choice=="9":
        revenue_report()
    elif choice=="10":
        export_bookings()
    elif choice=="11":
        print("Thank you!" \
              "visit again..")
        break
    else:
        print("Invalid choice")
    
