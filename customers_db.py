import sqlite3

class Customer:
    def __init__(self, ap_firstname, ap_lastname, ap_mobile, ap_email):
        self.firstname=ap_firstname
        self.lastname=ap_lastname
        self.mobile=ap_mobile
        self.email=ap_email

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            firstname TEXT,
            lastname TEXT,
            mobile INTEGER,
            email TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """   
            DROP TABLE IF EXISTS customers;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = """
            INSERT INTO customers (firstname, lastname, mobile, email)
            VALUES (?, ?, ?, ?)
        """
        CURSOR.execute(sql, (self.firstname, self.lastname, self.mobile, self.email))
        CONN.commit()

        self.id = CURSOR.lastrowid

    def update(self):
        sql = """
            update customers set
                firstname = ?,
                lastname = ?,
                mobile = ?,
                email = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.firstname, self.lastname, self.mobile, self.email, self.id))
        CONN.commit()

    def delete(self):
        sql = """
            delete from customers 
            WHERE id=?
        """
        CURSOR.execute(sql,  (self.id, ))
        CONN.commit()

    @classmethod
    def create(cls, firstname, lastname, mobile, email):
        new_instance = cls(firstname, lastname, mobile, email)
        new_instance.save()

        return new_instance

    @classmethod
    def create_from_db(cls, table_row):
        new_instance = cls(table_row[1], table_row[2], table_row[3], table_row[4])
        new_instance.id = table_row[0]

        return new_instance

    @classmethod
    def get_table_rows(cls):
        sql = """    
            SELECT * FROM customers
        """
        table_rows = CURSOR.execute(sql).fetchall()

        return [cls.create_from_db(row) for row in table_rows]

    def change_firstname(self, ap_firstname):
        self.firstname=ap_firstname
        self.update()

    def change_lastname(self, ap_lastname):
        self.lastname=ap_lastname
        self.update()

    def change_mobile(self, ap_mobile):
        self.mobile=ap_mobile
        self.update()

    def change_email(self, ap_email):
        self.email=ap_email
        self.update()

    def __str__(self):
        return "ID: "+str(self.id)+" Ονομα: "+self.firstname+" Επωνυμο: "+self.lastname+" Κινητο: "+str(self.mobile)+" Email: "+self.email





class Appointment():
    '''Η κλάση Customer περιγράφει έναν πελατη και την μέθοδο __str__.'''
    def __init__(self, ap_customerid, ap_datetime, ap_duration=20):
        self.customerid=ap_customerid
        self.datetime=ap_datetime
        self.duration=ap_duration

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY,
            customerid INTEGER,
            datetime TEXT,
            duration INTEGER)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """   
            DROP TABLE IF EXISTS appointments;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = """
            INSERT INTO appointments (customerid, datetime, duration)
            VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (self.customerid, self.datetime, self.duration))
        CONN.commit()

        self.id = CURSOR.lastrowid

    def delete(self):
        sql = """
            delete from appointments 
            WHERE id=?
        """
        CURSOR.execute(sql,  (self.id, ))
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

    def __str__(self):
        return "ID: "+str(self.id)+" customerID: "+str(self.customerid)+" Ημερομηνια: "+self.datetime+" Διαρκεια: "+str(self.duration)


def menu_customer():
    while True:
        print("")
        print("Διαχειρηση πελατων:")
        print("1. Δημιουργεια πελατη")
        print("2. Τροποποιηση πελατη")
        print("3. Διαγραφη πελατη")
        print("99. Προηγουμενο menu")

        choice = input("Επιλογη: ")

        if choice == '1':
            customer_create()
        elif choice == '2':
            customer_modify()
        elif choice == '3':
            customer_delete()
        elif choice == '99':
            break
        else:
            print("Λαθος επιλογη. Παρακαλω επιλεξτε παλι.")

def customer_create():
    global customers
    ap_firstname = input("Ονομα: ")
    ap_lastname = input("Επωνυμο: ")
    ap_mobile = input("Κινητο : ")
    ap_email = input("Email: ")
    newcustomer=Customer.create(ap_firstname,ap_lastname,ap_mobile,ap_email)
    print(newcustomer)
    customers.append(newcustomer)


def customer_modify():
    global customers
    if len(customers) == 0:
        print("Δεν υπαρχουν πελατες. Επιστροφη στο προηγουμενο μενου.")
        return
    customerIDs = {}
    counter = 0
    for customer in customers:
        customerIDs[customer.id]=counter
        counter=counter+1

    while True:
        print("")
        print("Λιστα πελατων:")
        for customer in customers:
            print(customer)
        choice = int(input("Επιλεξτε το ID του πελατη που θελετε να τροποποιησετε η 99 για επιστροφη: "))

        if choice in customerIDs:
            print("Επιλεξατε τον πελατη: ")
            tmp=customers[customerIDs[choice]]
            print(tmp)

            while True:
                print("1. Αλλαγη Ονοματος")
                print("2. Αλλαγη Επωνυμου")
                print("3. Αλλαγη Κινητου")
                print("4. Αλλαγη Email")
                print("99. Προηγουμενο menu")

                choice = input("Επιλεξτε αλλαγη: ")

                if choice == '1':
                    tempinput = input("Νεο ονομα: ")
                    tmp.change_firstname(tempinput)
                    print(tmp)
                elif choice == '2':
                    tempinput = input("Νεο Επωνυμο: ")
                    tmp.change_lastname(tempinput)
                    print(tmp)
                elif choice == '3':
                    tempinput = input("Νεο Κινητο: ")
                    tmp.change_mobile(tempinput)
                    print(tmp)
                elif choice == '4':
                    tempinput = input("Νεο Email: ")
                    tmp.change_email(tempinput)
                    print(tmp)
                elif choice == '99':
                    break
                else:
                    print("Λαθος επιλογη. Παρακαλω επιλεξτε παλι.")
        elif choice == 99:
            break
        else:
            print("Λαθος επιλογη. Παρακαλω επιλεξτε παλι.")

def customer_delete():
    global customers
    if len(customers) == 0:
        print("Δεν υπαρχουν πελατες. Επιστροφη στο προηγουμενο μενου.")
        return
    customerIDs = {}
    counter = 0
    for customer in customers:
        customerIDs[customer.id] = counter
        counter = counter + 1

    while True:
        if len(customers) == 0:
            print("Δεν υπαρχουν πελατες. Επιστροφη στο προηγουμενο μενου.")
            break
        print("")
        print("Λιστα πελατων:")
        for customer in customers:
            print(customer)
        choice = int(input("Επιλεξτε το ID του πελατη που θελετε να διαγραψετε η 99 για επιστροφη: "))

        if choice in customerIDs:
            print("Διαγραψατε τον πελατη: ")
            tmp=customers[customerIDs[choice]]
            print(tmp)
            tmp.delete()
            customers.pop(customerIDs[choice])
        elif choice == 99:
            break
        else:
            print("Λαθος επιλογη. Παρακαλω επιλεξτε παλι.")

def menu_appointment():
    while True:
        print("")
        print("Διαχειρηση ραντεβου:")
        print("1. Δημιουργεια ραντεβου")
        print("2. Τροποποιηση ραντεβου")
        print("3. Διαγραφη ραντεβου")
        print("99. Προηγουμενο menu")

        choice = input("Επιλογη: ")

        if choice == '1':
            appointment_create()
        elif choice == '2':
            appointment_modify()
        elif choice == '3':
            appointment_delete()
        elif choice == '99':
            break
        else:
            print("Λαθος επιλογη. Παρακαλω επιλεξτε παλι.")

def appointment_create():
    global appointments
    ap_customerid = input("Πελατης: ")
    ap_date = input("Ημερα: ")
    ap_time = input("Ωρα : ")
    ap_duration = input("Διαρκεια: ")
    newappointment=Appointment.create(ap_customerid,ap_date+" "+ap_time, ap_duration)
    print(newappointment)
    appointments.append(newappointment)

def appointment_modify():
    global customers
    global appointments

    #if len(customers) == 0:
    #    print("Δεν υπαρχουν πελατες. Επιστροφη στο προηγουμενο μενου.")
    #    return

    if len(appointments) == 0:
        print("Δεν υπαρχουν ραντεβου. Επιστροφη στο προηγουμενο μενου.")
        return

    customerIDs = {}
    counter = 0
    for customer in customers:
        customerIDs[customer.id]=counter
        counter=counter+1

    appointmentIDs = {}
    counter = 0
    for appointment in appointments:
        appointmentIDs[appointment.id]=counter
        counter=counter+1


    while True:
        print("")
        print("Λιστα ραντεβου:")
        for appointment in appointments:
            print(appointment)
        choice = int(input("Επιλεξτε το ID του ραντεβου που θελετε να τροποποιησετε η 99 για επιστροφη: "))

        if choice in appointmentIDs:
            print("Επιλεξατε το ραντεβου: ")
            tmp=customers[customerIDs[choice]]
            print(tmp)

            while True:
                print("1. Αλλαγη Πελατη")
                print("2. Αλλαγη Ημερας")
                print("3. Αλλαγη Ωρας")
                print("4. Αλλαγη Διαρκειας")
                print("99. Προηγουμενο menu")

                choice = input("Επιλεξτε αλλαγη: ")

                if choice == '1':
                    tempinput = input("Νεος πελατης: ")
                    tmp.changecustomerid(tempinput)
                    print(tmp)
                elif choice == '2':
                    tempinput = input("Νεα ημερα: ")
                    tmp.changedate(tempinput)
                    print(tmp)
                elif choice == '3':
                    tempinput = input("Νεα Ωρα: ")
                    tmp.changetime(tempinput)
                    print(tmp)
                elif choice == '4':
                    tempinput = input("Νεα Διαρκεια: ")
                    tmp.changeduration(tempinput)
                    print(tmp)
                elif choice == '99':
                    break
                else:
                    print("Λαθος επιλογη. Παρακαλω επιλεξτε παλι.")
        elif choice == 99:
            break
        else:
            print("Λαθος επιλογη. Παρακαλω επιλεξτε παλι.")

def appointment_delete():
    global appointments
    if len(appointments) == 0:
        print("Δεν υπαρχουν ραντεβου. Επιστροφη στο προηγουμενο μενου.")
        return
    appointmentIDs = {}
    counter = 0
    for appointment in appointments:
        appointmentIDs[appointment.id] = counter
        counter = counter + 1

    while True:
        if len(appointments) == 0:
            print("Δεν υπαρχουν ραντεβου. Επιστροφη στο προηγουμενο μενου.")
            break
        print("")
        print("Λιστα ραντεβου:")
        for appointment in appointments:
            print(appointment)
        choice = int(input("Επιλεξτε το ID του ραντεβου που θελετε να διαγραψετε η 99 για επιστροφη: "))

        if choice in appointmentIDs:
            print("Διαγραψατε το ραντεβου: ")
            tmp=appointments[appointmentIDs[choice]]
            print(tmp)
            tmp.delete()
            appointments.pop(appointmentIDs[choice])
        elif choice == 99:
            break
        else:
            print("Λαθος επιλογη. Παρακαλω επιλεξτε παλι.")

def menu_main():
        while True:
            print("")
            print("Κεντρικο Menu:")
            print("1. Διαχειρηση πελατων")
            print("2. Διαχειρηση ραντεβου")
            print("3. Αναζητηση")
            print("4. Υπενθυμιση")
            print("5. Εκτυπωση")
            print("99. Εξοδος προγραμματος")

            choice = input("Επιλογη: ")

            if choice == '1':
                menu_customer()
            elif choice == '2':
                menu_appointment()
            elif choice == '3':
                menu_search()
            elif choice == '4':
                menu_notification()
            elif choice == '5':
                menu_printout()
            elif choice == '99':
                print("Εξοδος απο το προγραμμα")
                break
            else:
                print("Λαθος επιλογη. Παρακαλω επιλεξτε παλι.")



if __name__ == '__main__':

    # sqlite3 has a connect() method which accepts a .db file as a destination
    CONN = sqlite3.connect('apointments.db')

    # once we establish our connection and assign it to CONN, we create a CURSOR
    CURSOR = CONN.cursor()

    #Customer.drop_table()
    #Appointment.drop_table()
    Customer.create_table()
    Appointment.create_table()

    customers = Customer.get_table_rows()
    appointments = Appointment.get_table_rows()

    menu_main()