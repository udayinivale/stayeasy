from datetime import timedelta

def calculate_total_amount(room,guest_count,check_in,check_out,breakfast_choice="no",completed_stays=0):
    breakfast_amount=0
    total=0
    room_total=0
    extra_total=0
    breakfast_total=0
    gst_total=0
    night_charges=[]

    days=(check_out-check_in).days

    if room.room_type=="standard" and breakfast_choice=="yes":
        breakfast_amount=guest_count*350

    for day in range(days):
        current_date=check_in+timedelta(days=day)
        room_charge=room.tariff()
        if current_date.weekday() in [4,5]:
            room_charge=room_charge+(room_charge*0.20)

        extra_charge=room.extra_guest_charges(guest_count)

        room_total+=room_charge
        extra_total+=extra_charge
        breakfast_total+=breakfast_amount
        night_charges.append((room_charge,extra_charge,breakfast_amount))

    long_stay_discount=0
    loyalty_discount=0

    if days>=7:
        long_stay_discount=room_total*0.10
    remaining_room_total=room_total-long_stay_discount

    if completed_stays>=3:
        loyalty_discount=remaining_room_total*0.05
    total_discount=long_stay_discount+loyalty_discount

    for room_charge,extra_charge,breakfast_amount in night_charges:
        if room_total>0:
            night_discount=(room_charge/room_total)*total_discount
        else:
            night_discount=0
        taxable_amount=room_charge-night_discount+extra_charge+breakfast_amount
        
        if room_charge>7500:
            gst=taxable_amount*0.18
        else:
            gst=taxable_amount*0.12
        gst_total+=gst

    total=room_total+extra_total+breakfast_total-total_discount+gst_total
    return total, room_total, extra_total, breakfast_total, long_stay_discount, loyalty_discount, gst_total, night_charges