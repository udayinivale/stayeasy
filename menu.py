def show_menu(search_availability, create_booking, check_in, check_out, cancel_booking_room, view_booking, view_guest_history, occupancy_report, revenue_report, export_bookings):
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
            print("Thank you! visit again..")
            break
        else:
            print("Invalid choice")
