import sqlite3
import customers
import appointments
import utils

def menu_appointment():
    while True:
        print("")
        print("Διαχειρηση ραντεβου:")
        print("1. Δημιουργεια ραντεβου")
        print("2. Τροποποιηση ραντεβου")
        print("3. Διαγραφη ραντεβου")
        print("99. Προηγουμενο menu")

        choice = utils.get_number("Επιλογη: ")

        if choice == '1':
            menu_appointment_create()
        elif choice == '2':
            menu_appointment_modify()
        elif choice == '3':
            menu_appointment_delete()
        elif choice == '99':
            break
        else:
            print("Λαθος επιλογη. Παρακαλω επιλεξτε παλι.")


def menu_appointment_create():
    if customers.no_customers():
        print("Δεν υπαρχουν πελατες. Επιστροφη στο προηγουμενο μενου.")
        return

    customers_list = customers.Customer.get_table_rows()

    appointments_list = appointments.Appointment.get_table_rows()

    customerIDs = {}
    counter = 0
    for customer in customers_list:
        customerIDs[customer.id] = counter
        counter = counter + 1

    while True:
        print("")
        print("Λιστα πελατων:")
        for customer in customers_list:
            print(customer)

        ap_customerid = int(utils.get_number("Επιλεξτε το ID του πελατη: "))
        if ap_customerid in customerIDs:
            print("Επιλεξατε τον πελατη: ")
            tmp = customers_list[customerIDs[ap_customerid]]
            print(tmp)
            break
        else:
            print("Λαθος επιλογη. Παρακαλω επιλεξτε παλι.")

    ap_datetime = utils.get_datetime("Ημερομηνια/Ωρα σε μορφη <Ετος>-<Μηνας>-<Ημερα> <Ωρα>:<Λεπτα> : ")

    ap_duration = utils.get_number("Διαρκεια: ")
    newappointment = appointments.Appointment.create(ap_customerid, ap_datetime, ap_duration)
    # print(newappointment)
    appointment_row = appointments.appointment_by_id_with_customer_fullname(newappointment.id)
    #print(appointment_row)
    print("ID: " + str(appointment_row[0]) + " Full Name: " + str(appointment_row[1]) + " " + str(
        appointment_row[2]) + " Ημερομηνια: " + str(appointment_row[3]) + " Διαρκεια: " + str(appointment_row[4]))
    appointments_list.append(newappointment)


def menu_appointment_modify():
    if customers.no_customers():
        print("Δεν υπαρχουν πελατες. Επιστροφη στο προηγουμενο μενου.")
        return

    if appointments.no_appointments():
        print("Δεν υπαρχουν ραντεβου. Επιστροφη στο προηγουμενο μενου.")
        return

    customers_list = customers.Customer.get_table_rows()
    appointments_list = appointments.Appointment.get_table_rows()
    customerIDs = {}
    counter = 0
    for customer in customers_list:
        customerIDs[customer.id] = counter
        counter = counter + 1

    appointmentIDs = {}
    counter = 0
    for appointment in appointments_list:
        appointmentIDs[appointment.id] = counter
        counter = counter + 1

    while True:
        print("")
        print("Λιστα ραντεβου:")
        # for appointment in appointments_list:
        #    print(appointment)
        appointments_tablerows = appointments.list_appointments_with_customer_fullname()
        for appointment_row in appointments_tablerows:
            # print(appointment_row)
            print("ID: " + str(appointment_row[0]) + " Full Name: " + str(appointment_row[1]) + " " + str(
                appointment_row[2]) + " Ημερομηνια: " + str(appointment_row[3]) + " Διαρκεια: " + str(appointment_row[4]))
        choice = int(utils.get_number("Επιλεξτε το ID του ραντεβου που θελετε να τροποποιησετε η 99 για επιστροφη: "))

        if choice in appointmentIDs:
            print("Επιλεξατε το ραντεβου: ")
            tmp = appointments_list[appointmentIDs[choice]]
            print(tmp)

            while True:
                print("1. Αλλαγη Πελατη")
                print("2. Αλλαγη Ημεραμηνιας/Ωρας")
                # print("3. Αλλαγη Ωρας")
                print("4. Αλλαγη Διαρκειας")
                print("99. Προηγουμενο menu")

                choice = utils.get_number("Επιλεξτε αλλαγη: ")

                if choice == '1':
                    while True:
                        print("")
                        print("Λιστα πελατων:")
                        for customer in customers_list:
                            print(customer)

                        ap_customerid = int(utils.get_number("Επιλεξτε το ID του πελατη: "))
                        if ap_customerid in customerIDs:
                            print("Επιλεξατε τον πελατη: ")
                            print(customers_list[customerIDs[ap_customerid]])
                            break
                        else:
                            print("Λαθος επιλογη. Παρακαλω επιλεξτε παλι.")
                    tmp.change_customerid(ap_customerid)
                    print("")
                    appointment_row = appointments.appointment_by_id_with_customer_fullname(tmp.id)
                    # print(appointment_row)
                    print("ID: " + str(appointment_row[0]) + " Full Name: " + str(appointment_row[1]) + " " + str(
                        appointment_row[2]) + " Ημερομηνια: " + str(appointment_row[3]) + " Διαρκεια: " + str(
                        appointment_row[4]))
                elif choice == '2':
                    tempinput = utils.get_datetime("Νεα ημεραμηνια/ωρα: ")
                    tmp.change_datetime(tempinput)
                    print("")
                    appointment_row = appointments.appointment_by_id_with_customer_fullname(tmp.id)
                    # print(appointment_row)
                    print("ID: " + str(appointment_row[0]) + " Full Name: " + str(appointment_row[1]) + " " + str(
                        appointment_row[2]) + " Ημερομηνια: " + str(appointment_row[3]) + " Διαρκεια: " + str(
                        appointment_row[4]))
                # elif choice == '3':
                #    tempinput = input("Νεα Ωρα: ")
                #    tmp.change_datetime(tempinput)
                #    print(tmp)
                elif choice == '4':
                    tempinput = utils.get_number("Νεα Διαρκεια: ")
                    tmp.change_duration(tempinput)
                    print("")
                    appointment_row = appointments.appointment_by_id_with_customer_fullname(tmp.id)
                    # print(appointment_row)
                    print("ID: " + str(appointment_row[0]) + " Full Name: " + str(appointment_row[1]) + " " + str(
                        appointment_row[2]) + " Ημερομηνια: " + str(appointment_row[3]) + " Διαρκεια: " + str(
                        appointment_row[4]))
                elif choice == '99':
                    break
                else:
                    print("Λαθος επιλογη. Παρακαλω επιλεξτε παλι.")
        elif choice == 99:
            break
        else:
            print("Λαθος επιλογη. Παρακαλω επιλεξτε παλι.")


def menu_appointment_delete():

    if appointments.no_appointments():
        print("Δεν υπαρχουν ραντεβου. Επιστροφη στο προηγουμενο μενου.")
        return

    appointments_list = appointments.Appointment.get_table_rows()
    appointmentIDs = {}
    counter = 0
    for appointment in appointments_list:
        appointmentIDs[appointment.id] = counter
        counter = counter + 1

    while True:
        if appointments.no_appointments():
            print("Δεν υπαρχουν ραντεβου. Επιστροφη στο προηγουμενο μενου.")
            break
        print("")
        print("Λιστα ραντεβου:")
        # for appointment in appointments_list:
        #    print(appointment)
        appointments_tablerows = appointments.list_appointments_with_customer_fullname()
        for appointment_row in appointments_tablerows:
            # print(appointment_row)
            print("ID: " + str(appointment_row[0]) + " Full Name: " + str(appointment_row[1]) + " " + str(
                appointment_row[2]) + " Ημερομηνια: " + str(appointment_row[3]) + " Διαρκεια: " + str(appointment_row[4]))
        choice = int(utils.get_number("Επιλεξτε το ID του ραντεβου που θελετε να διαγραψετε η 99 για επιστροφη: "))

        if choice in appointmentIDs:
            print("Διαγραψατε το ραντεβου: ")
            appointment_row = appointments.appointment_by_id_with_customer_fullname(appointments_list[appointmentIDs[choice]].id)
            # print(appointment_row)
            print("ID: " + str(appointment_row[0]) + " Full Name: " + str(appointment_row[1]) + " " + str(
                appointment_row[2]) + " Ημερομηνια: " + str(appointment_row[3]) + " Διαρκεια: " + str(
                appointment_row[4]))
            tmp = appointments_list[appointmentIDs[choice]]
            tmp.delete()
            appointments_list.pop(appointmentIDs[choice])
        elif choice == 99:
            break
        else:
            print("Λαθος επιλογη. Παρακαλω επιλεξτε παλι.")
