import sqlite3
import csv
conn=sqlite3.connect("stayeasy.db")
cursor=conn.cursor()
def create_tables():
    # cursor.execute("DROP TABLE IF EXISTS bookings")
    # cursor.execute("DROP TABLE IF EXISTS guests")
    # cursor.execute("DROP TABLE IF EXISTS rooms")
    # conn.commit()
    cursor.execute("""
        create table if not exists rooms(
        room_no int primary key,
        room_type text,
        floor int)
        """) 
    conn.commit() 
    cursor.execute("""create table if not exists guests(
        name text not null,
        mobile_num text primary key,
        email text not null)
        """)     
    conn.commit() 
    cursor.execute("""create table if not exists bookings(
        booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
        mobile_num text,
        room_no int,
        check_in text,
        check_out text,
        breakfast_choice text,
        guest_count int,
        completed_stays int,
        booking_status text,
        total_amount real,
        foreign key(mobile_num) references guests(mobile_num),
        foreign key(room_no) references rooms(room_no))
        """)
    conn.commit()
   

def load_rooms():
    with open("rooms.csv","r",newline='') as file,open("app.log",'w',newline='')as errors:
        rooms=list(csv.DictReader(file))
        errors_file=[]
        valid_data=[]
        room_no=set()
        for row in rooms:
            # print(row) 
            current_room=row['room_no'].strip()
            room_type=row['room_type'].strip().lower()
            try:
                if int(current_room)<=0:
                    errors_file.append(f"{row}:invalid room no")
                    continue
            except ValueError:
                errors_file.append(f"{row}:invalid room no")
                continue
            current_room=int(current_room)
            if current_room in room_no:
                errors_file.append(f"{row}:duplicate room no")
                continue
            if room_type not in ['standard','deluxe','suite']:
                errors_file.append(f"{row}:invalid room type")
                continue

            room_no.add(current_room)
            valid_data.append(row)

        for error in errors_file:
                errors.write(error)
        
        for row in valid_data:
            cursor.execute("insert or ignore into rooms values(?,?,?)",
                (int(row['room_no']),row['room_type'],int(row['floor'])))
        conn.commit()
       

    return valid_data

def add_guest(name,mobile_num,email):
    cursor.execute("insert or ignore into guests values(?,?,?)",
                (name,mobile_num,email))
    conn.commit()
    

def add_bookings(mobile_num,room_no,check_in,check_out,guest_count,total_amount,breakfast_choice,completed_stays):
    conn=sqlite3.connect("stayeasy.db")
    cursor=conn.cursor()
    
    cursor.execute("""
    insert into bookings(mobile_num,room_no,check_in,check_out,guest_count,booking_status,total_amount,breakfast_choice,completed_stays)
    values(?,?,?,?,?,?,?,?,?)""",
    (mobile_num,room_no,check_in,check_out,guest_count,"confirmed",total_amount,breakfast_choice,completed_stays))
    last_id=cursor.lastrowid
    booking_id=f"BK{last_id:04d}"
    conn.commit()
   
    return booking_id

def check_availability(room_type,check_in,check_out):

    cursor.execute("""select room_no from bookings
    where booking_status in('confirmed','checked_in')
    and check_in<?
    and check_out>?
    """,(check_out,check_in))

    occupied_rooms=cursor.fetchall()
   
    return occupied_rooms

def check_in_booking(booking_id):
    
    booking_id=booking_id.strip().upper()
    if not booking_id.startswith("BK") or not booking_id[2:].isdigit():
        conn.close()
        return "invalid booking id"
    booking_id=int(booking_id[2:])
    cursor.execute("select booking_status from bookings where booking_id=?",(booking_id,))
    result=cursor.fetchone()
    if result is None:
        print("no booking id found")
    if result[0]!="confirmed":
        conn.close()
        return "cannot check in."
    cursor.execute("update bookings set booking_status=? where booking_id=?",("checked_in",booking_id))
    conn.commit()
    return "checked-in successfully"

def check_out_booking(booking_id):
    
    booking_id=booking_id.strip().upper()
    if not booking_id.startswith("BK") or not booking_id[2:].isdigit():
        return "invalid booking id"
    booking_id=int(booking_id[2:])
    cursor.execute("select booking_status from bookings where booking_id=?",(booking_id,))
    result=cursor.fetchone()
    if result is None:
        return "no booking id found"
    if result[0]!="checked_in":
        return "cannot check out."
    cursor.execute("update bookings set booking_status=? where booking_id=?",("checked_out",booking_id))
    conn.commit()
    return "checked-out successfully"
def cancel_booking(booking_id):
    booking_id=booking_id.strip().upper()

    if not booking_id.startswith("BK") or not booking_id[2:].isdigit():
        return "invalid booking id"
    booking_id=int(booking_id[2:])

    cursor.execute("select booking_status,check_in,total_amount from bookings where booking_id=?",(booking_id,))
    result=cursor.fetchone()
    if result is None:
        return "no booking id found"
    booking_status,check_in,total_amount=result

    if booking_status!="confirmed":
        return "only confirmed bookings can be cancelled"

    from datetime import datetime,date
    check_in=datetime.strptime(check_in,"%d-%m-%Y").date()
    days_left=(check_in-date.today()).days

    if days_left>=7:
        refund=total_amount
    elif days_left>=2:
        refund=total_amount*0.50
    else:
        refund=0
    refund_amount=total_amount-refund
    cursor.execute("update bookings set booking_status=? where booking_id=?",("cancelled",booking_id))
    conn.commit()
    return refund,refund_amount

def count_completed_stays(mobile_num):

    cursor.execute("select count(*) from bookings where mobile_num=? and booking_status='checked_out'",(mobile_num,))
    result=cursor.fetchone()
    return result[0]

def guest_stay_history(mobile_num):
    cursor.execute("""
    select booking_id,room_no,check_in,check_out,booking_status,total_amount
    from bookings
    where mobile_num=?
    order by booking_id
    """,(mobile_num,))
    result=cursor.fetchall()
    return result

def view_booking_details(booking_id):
    booking_id=booking_id.strip().upper()
    if not booking_id.startswith("BK") or not booking_id[2:].isdigit():
        return None

    booking_id=int(booking_id[2:])
    cursor.execute("""
    select b.booking_id,g.name,g.mobile_num,g.email,
    b.room_no,r.room_type,b.check_in,b.check_out,
    b.guest_count,b.booking_status,b.total_amount,
    b.breakfast_choice,b.completed_stays
    from bookings b
    join guests g on b.mobile_num=g.mobile_num
    join rooms r on b.room_no=r.room_no
    where b.booking_id=?
    """,(booking_id,))
    result=cursor.fetchone()
    return result