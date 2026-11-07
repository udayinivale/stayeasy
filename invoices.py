from database import view_booking_details
from pricing import calculate_total_amount
from models import Standardroom,Deluxeroom,Suiteroom
from datetime import datetime,timedelta

def generate_invoice(booking_id):
    booking=view_booking_details(booking_id)

    if booking is None:
        print("Booking details not found")
        return
    booking_id,name,mobile_num,email,room_no,room_type,check_in,check_out,guest_count,booking_status,total_amount,breakfast_choice,completed_stays=booking
    room_type=room_type.lower().strip()
    if room_type=="standard":
        room=Standardroom(room_no,room_type,1)
    elif room_type=="deluxe":
        room=Deluxeroom(room_no,room_type,2)
    else:
        room=Suiteroom(room_no,room_type,3)

    check_in=datetime.strptime(check_in,"%d-%m-%Y").date()
    check_out=datetime.strptime(check_out,"%d-%m-%Y").date()
    

    result=calculate_total_amount(room,guest_count,check_in,check_out,breakfast_choice,completed_stays) 
    total,room_total,extra_total,breakfast_total,long_stay_discount,loyalty_discount,gst_total,night_charges=result
    with open(f"invoices/BK{booking_id:04d}.txt","w") as file: 
        file.write("Hotel Invoice\n")     
        file.write("-----------------------------\n")
        file.write(f"Booking ID: BK{booking_id:04d}\n")      
        file.write(f"Guest Name: {name}\n")
        file.write(f"Mobile Number: {mobile_num}\n")
        file.write(f"Email: {email}\n")
        file.write(f"Room Number: {room_no}\n")
        file.write(f"Room Type: {room_type}\n")
        file.write(f"Guest Count: {guest_count}\n")
        file.write(f"Check-in: {check_in}\n")
        file.write(f"Check-out: {check_out}\n")
        file.write(f"Booking Status: {booking_status}\n")
        file.write("-----------------------------\n")
        file.write("\nNight-wise Charges\n")
        file.write("-----------------------------\n")

        for day in range(len(night_charges)):
            current_date=check_in+timedelta(days=day)
            room_charge,extra_charge,breakfast_amount=night_charges[day]

            file.write(f"\nDate: {current_date}\n")
            file.write(f"Room Charge: Rs.{room_charge:.2f}\n")
            file.write(f"Extra Guest Charge: Rs.{extra_charge:.2f}\n")
            file.write(f"Breakfast Charge: Rs.{breakfast_amount:.2f}\n")
            file.write("\n-----------------------------\n")
        file.write("Price Summary\n")
        file.write("-----------------------------\n")
        file.write(f"Room Charges: Rs.{room_total:.2f}\n")
        file.write(f"Extra Guest Charges: Rs.{extra_total:.2f}\n")
        file.write(f"Breakfast Charges: Rs.{breakfast_total:.2f}\n")
        file.write(f"Long Stay Discount: Rs.{long_stay_discount:.2f}\n")
        file.write(f"Loyalty Discount: Rs.{loyalty_discount:.2f}\n")
        file.write(f"GST: Rs.{gst_total:.2f}\n")
        file.write("-----------------------------\n")
        file.write(f"Total Amount: Rs.{total:.2f}\n")
        file.write("-----------------------------\n")