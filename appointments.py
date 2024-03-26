import sqlite3
import customers


def create_table():
    sql = """
        CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY,
        customerid INTEGER,
        datetime TEXT,
        duration INTEGER)
    """
    CURSOR.execute(sql)
    CONN.commit()


def drop_table():
    sql = """   
        DROP TABLE IF EXISTS appointments;
    """
    CURSOR.execute(sql)
    CONN.commit()


# sqlite3 has a connect() method which accepts a .db file as a destination
CONN = sqlite3.connect('appointments.db')

# once we establish our connection and assign it to CONN, we create a CURSOR
CURSOR = CONN.cursor()

# drop_table()
create_table()


class Appointment():
    '''Η κλάση Customer περιγράφει έναν πελατη και την μέθοδο __str__.'''

    def __init__(self, ap_customerid, ap_datetime, ap_duration=20):
        self.customerid = ap_customerid
        self.datetime = ap_datetime
        self.duration = ap_duration

    def save(self):
        sql = """
            INSERT INTO appointments (customerid, datetime, duration)
            VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (self.customerid, self.datetime, self.duration))
        CONN.commit()

        self.id = CURSOR.lastrowid

    def update(self):
        sql = """
            update appointments set
                customerid = ?,
                datetime = ?,
                duration = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.customerid, self.datetime, self.duration, self.id))
        CONN.commit()

    def delete(self):
        sql = """
            delete from appointments 
            WHERE id=?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

    @classmethod
    def create(cls, ap_customerid, ap_datetime, ap_duration):
        new_instance = cls(ap_customerid, ap_datetime, ap_duration)
        new_instance.save()

        return new_instance

    @classmethod
    def create_from_db(cls, table_row):
        new_instance = cls(table_row[1], table_row[2], table_row[3])
        new_instance.id = table_row[0]

        return new_instance

    @classmethod
    def get_table_rows(cls):
        sql = """    
            SELECT * FROM appointments
        """
        table_rows = CURSOR.execute(sql).fetchall()

        return [cls.create_from_db(row) for row in table_rows]

    def change_customerid(self, ap_customerid):
        self.customerid = ap_customerid
        self.update()

    def change_datetime(self, ap_datetime):
        self.datetime = ap_datetime
        self.update()

    def change_duration(self, ap_duration):
        self.duration = ap_duration
        self.update()

    def __str__(self):
        return "ID: " + str(self.id) + " customerID: " + str(
            self.customerid) + " Ημερομηνια: " + self.datetime + " Διαρκεια: " + str(self.duration)




def list_appointments_with_customer_fullname():
    sql = """
        select app.id,cust.firstname,cust.lastname,app.datetime,app.duration from appointments app
        left join customers cust on app.customerid=cust.id
    """
    table_rows = CURSOR.execute(sql).fetchall()
    return table_rows


def appointment_by_id_with_customer_fullname(ap_appointmentid):
    sql = """
        select app.id,cust.firstname,cust.lastname,app.datetime,app.duration from appointments app
        join customers cust on app.customerid=cust.id
        where app.id = ?
    """
    return CURSOR.execute(sql, (ap_appointmentid,)).fetchone()


def appointment_create():
    if customers.no_customers == True:
        print("Δεν υπαρχουν πελατες. Επιστροφη στο προηγουμενο μενου.")
        return

    customers_list = customers.Customer.get_table_rows()

    appointments_list = Appointment.get_table_rows()

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

        ap_customerid = int(input("Επιλεξτε το ID του πελατη: "))
        if ap_customerid in customerIDs:
            print("Επιλεξατε τον πελατη: ")
            tmp = customers_list[customerIDs[ap_customerid]]
            print(tmp)
            break
        else:
            print("Λαθος επιλογη. Παρακαλω επιλεξτε παλι.")

    ap_date = input("Ημερα: ")
    ap_time = input("Ωρα : ")
    ap_duration = input("Διαρκεια: ")
    newappointment = Appointment.create(ap_customerid, ap_date + " " + ap_time, ap_duration)
    # print(newappointment)
    appointment_row = appointment_by_id_with_customer_fullname(newappointment.id)
    #print(appointment_row)
    print("ID: " + str(appointment_row[0]) + " Full Name: " + str(appointment_row[1]) + " " + str(
        appointment_row[2]) + " Ημερομηνια: " + str(appointment_row[3]) + " Διαρκεια: " + str(appointment_row[4]))
    appointments_list.append(newappointment)


def appointment_modify():
    if customers.no_customers == True:
        print("Δεν υπαρχουν πελατες. Επιστροφη στο προηγουμενο μενου.")
        return

    customers_list = customers.Customer.get_table_rows()

    appointments_list = Appointment.get_table_rows()
    if len(appointments_list) == 0:
        print("Δεν υπαρχουν ραντεβου. Επιστροφη στο προηγουμενο μενου.")
        return

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
        appointments_tablerows = list_appointments_with_customer_fullname()
        for appointment_row in appointments_tablerows:
            # print(appointment_row)
            print("ID: " + str(appointment_row[0]) + " Full Name: " + str(appointment_row[1]) + " " + str(
                appointment_row[2]) + " Ημερομηνια: " + str(appointment_row[3]) + " Διαρκεια: " + str(appointment_row[4]))
        choice = int(input("Επιλεξτε το ID του ραντεβου που θελετε να τροποποιησετε η 99 για επιστροφη: "))

        if choice in appointmentIDs:
            print("Επιλεξατε το ραντεβου: ")
            tmp = appointments_list[appointmentIDs[choice]]
            print(tmp)

            while True:
                print("1. Αλλαγη Πελατη")
                print("2. Αλλαγη Ημεραμηνιας")
                # print("3. Αλλαγη Ωρας")
                print("4. Αλλαγη Διαρκειας")
                print("99. Προηγουμενο menu")

                choice = input("Επιλεξτε αλλαγη: ")

                if choice == '1':
                    while True:
                        print("")
                        print("Λιστα πελατων:")
                        for customer in customers_list:
                            print(customer)

                        ap_customerid = int(input("Επιλεξτε το ID του πελατη: "))
                        if ap_customerid in customerIDs:
                            print("Επιλεξατε τον πελατη: ")
                            print(customers_list[customerIDs[ap_customerid]])
                            break
                        else:
                            print("Λαθος επιλογη. Παρακαλω επιλεξτε παλι.")
                    tmp.change_customerid(ap_customerid)
                    print("")
                    appointment_row = appointment_by_id_with_customer_fullname(tmp.id)
                    # print(appointment_row)
                    print("ID: " + str(appointment_row[0]) + " Full Name: " + str(appointment_row[1]) + " " + str(
                        appointment_row[2]) + " Ημερομηνια: " + str(appointment_row[3]) + " Διαρκεια: " + str(
                        appointment_row[4]))
                elif choice == '2':
                    tempinput = input("Νεα ημεραμηνια: ")
                    tmp.change_datetime(tempinput)
                    print("")
                    appointment_row = appointment_by_id_with_customer_fullname(tmp.id)
                    # print(appointment_row)
                    print("ID: " + str(appointment_row[0]) + " Full Name: " + str(appointment_row[1]) + " " + str(
                        appointment_row[2]) + " Ημερομηνια: " + str(appointment_row[3]) + " Διαρκεια: " + str(
                        appointment_row[4]))
                # elif choice == '3':
                #    tempinput = input("Νεα Ωρα: ")
                #    tmp.change_datetime(tempinput)
                #    print(tmp)
                elif choice == '4':
                    tempinput = input("Νεα Διαρκεια: ")
                    tmp.change_duration(tempinput)
                    print("")
                    appointment_row = appointment_by_id_with_customer_fullname(tmp.id)
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


def appointment_delete():
    appointments_list = Appointment.get_table_rows()
    if len(appointments_list) == 0:
        print("Δεν υπαρχουν ραντεβου. Επιστροφη στο προηγουμενο μενου.")
        return

    appointmentIDs = {}
    counter = 0
    for appointment in appointments_list:
        appointmentIDs[appointment.id] = counter
        counter = counter + 1

    while True:
        if len(appointments_list) == 0:
            print("Δεν υπαρχουν ραντεβου. Επιστροφη στο προηγουμενο μενου.")
            break
        print("")
        print("Λιστα ραντεβου:")
        # for appointment in appointments_list:
        #    print(appointment)
        appointments_tablerows = list_appointments_with_customer_fullname()
        for appointment_row in appointments_tablerows:
            # print(appointment_row)
            print("ID: " + str(appointment_row[0]) + " Full Name: " + str(appointment_row[1]) + " " + str(
                appointment_row[2]) + " Ημερομηνια: " + str(appointment_row[3]) + " Διαρκεια: " + str(appointment_row[4]))
        choice = int(input("Επιλεξτε το ID του ραντεβου που θελετε να διαγραψετε η 99 για επιστροφη: "))

        if choice in appointmentIDs:
            print("Διαγραψατε το ραντεβου: ")
            appointment_row = appointment_by_id_with_customer_fullname(appointments_list[appointmentIDs[choice]].id)
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


def appointment_search_bydate():
    appointments_list = Appointment.get_table_rows()
    if len(appointments_list) == 0:
        print("Δεν υπαρχουν ραντεβου. Επιστροφη στο προηγουμενο μενου.")
        return


def appointment_search_bycustomerid():
    appointments_list = Appointment.get_table_rows()
    if len(appointments_list) == 0:
        print("Δεν υπαρχουν ραντεβου. Επιστροφη στο προηγουμενο μενου.")
        return
