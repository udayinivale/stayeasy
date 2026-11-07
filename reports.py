from database import cursor
from datetime import datetime,timedelta
def occupancy_report():
    start_date=input("Enter start date:")
    end_date=input("Enter end date:")

    start_date=datetime.strptime(start_date,"%d-%m-%Y").date()
    end_date=datetime.strptime(end_date,"%d-%m-%Y").date()

    if end_date<=start_date:
        print("Invalid date range")
        return

    cursor.execute("select count(*) from rooms")
    total_rooms=cursor.fetchone()[0]

    cursor.execute("""
    select check_in,check_out
    from bookings
    where booking_status in ('confirmed','checked_in','checked_out')
    """)
    bookings=cursor.fetchall()

    current_date=start_date
    total_occupancy=0
    days_count=0

    while current_date<end_date:
        occupied_rooms=0

        for check_in,check_out in bookings:
            check_in=datetime.strptime(check_in,"%d-%m-%Y").date()
            check_out=datetime.strptime(check_out,"%d-%m-%Y").date()

            if check_in<=current_date<check_out:
                occupied_rooms+=1

        occupancy=(occupied_rooms/total_rooms)*100

        print("Date:",current_date)
        print("Occupied Rooms:",occupied_rooms)
        print("Total Rooms:",total_rooms)
        print("Occupancy:",round(occupancy,2),"%")
        print("-------------------------")

        total_occupancy+=occupancy
        days_count+=1
        current_date+=timedelta(days=1)

    if days_count>0:
        average_occupancy=total_occupancy/days_count
        print("Average Occupancy:",round(average_occupancy,2),"%")
    else:
        print("No dates available for the report")