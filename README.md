# StayEasy – Hotel Booking Management System

## Project Overview

StayEasy is a Python-based hotel booking management system. It allows users to search for room availability, create and manage bookings, check guests in and out, calculate booking charges, generate invoices, and view hotel reports.

The application uses SQLite to store room, guest, and booking information. Room details are initially loaded from a CSV file.

## Features

- Search for available rooms by room type and stay dates.
- Register guests and create bookings.
- Check guests in and check them out.
- Cancel bookings and calculate the applicable refund and retained amount.
- View booking details and guest stay history.
- Calculate room charges, extra-guest charges, breakfast charges, weekend charges, discounts, and GST.
- Generate an invoice after a successful checkout.
- Generate occupancy and revenue reports.
- Export booking information to a CSV file.

## Project Structure


stay/
├── hotels.py       # Main application and booking-related functions
├── menu.py         # Displays the application menu and handles user choices
├── models.py       # Room, guest, and booking classes
├── database.py     # SQLite database setup and database operations
├── pricing.py      # Booking price, discounts, and GST calculations
├── invoices.py     # Invoice generation
├── reports.py      # Occupancy and revenue reports
├── exceptions.py   # Custom exception classes
├── rooms.csv       # Initial room data
├── stayeasy.db     # SQLite database
├── app.log         # Application log file
├── bookings.csv    # Exported booking data
└── invoices/       # Generated invoice text files


## Requirements

- Python 3
- SQLite
- Python standard library modules such as:
  - sqlite3
  - csv
  - datetime
  - re
  - os

No third-party packages are required for the current implementation.

## How to Run

1. Open a terminal in the project folder.
2. Activate your virtual environment if you are using one.
3. Run the main application:
4. Choose an option from the menu and follow the prompts.

## Application Menu

1. Search availability
2. Create booking
3. Check in
4. Check out
5. Cancel booking
6. View booking details
7. Guest stay history
8. Occupancy report
9. Revenue report
10. Export bookings
11. Exit

## Data Storage

- `rooms.csv` contains the initial room information.
- `stayeasy.db` stores room, guest, and booking records.
- `bookings.csv` is generated when the export option is selected.
- The `invoices/` folder stores invoice text files generated after successful checkout.
- `app.log` stores application log messages.

## Notes

- Run the application from the project folder so that its relative file paths resolve correctly.
- Keep the database file if you want to retain existing booking data.
- Do not delete or recreate the database when it contains records you want to keep.