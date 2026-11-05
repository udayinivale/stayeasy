import sqlite3
import csv

def create_tables():
    conn=sqlite3.connect("stayeasy.db")
    cursor=conn.cursor()
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
        guest_count int,
        booking_status text,
        total_amount real,
        foreign key(mobile_num) references guests(mobile_num),
        foreign key(room_no) references rooms(room_no))
        """)
    conn.commit()
    conn.close()

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
        conn=sqlite3.connect("stayeasy.db")
        cursor=conn.cursor()
        for row in valid_data:
            cursor.execute("insert or ignore into rooms values(?,?,?)",
                (int(row['room_no']),row['room_type'],int(row['floor'])))
        conn.commit()
        conn.close()

    return valid_data

def add_guest(name,mobile_num,email):
    conn=sqlite3.connect("stayeasy.db")
    cursor=conn.cursor()
    
    cursor.execute("insert or ignore into guests values(?,?,?)",
                (name,mobile_num,email))
    conn.commit()
    conn.close()

def add_bookings(mobile_num,room_no,check_in,check_out,guest_count,total_amount):
    conn=sqlite3.connect("stayeasy.db")
    cursor=conn.cursor()
    
    cursor.execute("""
    insert into bookings(mobile_num,room_no,check_in,check_out,guest_count,booking_status,total_amount)
    values(?,?,?,?,?,?,?)""",
    (mobile_num,room_no,check_in,check_out,guest_count,"confirmed",total_amount))
    last_id=cursor.lastrowid
    booking_id=f"BK{last_id:04d}"
    conn.commit()
    conn.close()
    return booking_id

def check_availability(room_type,check_in,check_out):
    conn=sqlite3.connect("stayeasy.db")
    cursor=conn.cursor()

    cursor.execute("""select room_no from bookings
    where booking_status in('confirmed','checked_in')
    and check_in<?
    and check_out>?
    """,(check_out,check_in))

    occupied_rooms=cursor.fetchall()
    conn.close()
    return occupied_rooms
    