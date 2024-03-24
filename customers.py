import sqlite3

def create_table():
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


def drop_table():
    sql = """   
        DROP TABLE IF EXISTS customers;
    """
    CURSOR.execute(sql)
    CONN.commit()

# sqlite3 has a connect() method which accepts a .db file as a destination
CONN = sqlite3.connect('appointments.db')

# once we establish our connection and assign it to CONN, we create a CURSOR
CURSOR = CONN.cursor()

# Customer.drop_table()
create_table()

class Customer:
    def __init__(self, ap_firstname, ap_lastname, ap_mobile, ap_email):
        self.firstname=ap_firstname
        self.lastname=ap_lastname
        self.mobile=ap_mobile
        self.email=ap_email


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

def delete_appointments_of_customerid(ap_customerid):
    sql = """
        delete from appointments 
        WHERE customerid=?
    """
    CURSOR.execute(sql,  (ap_customerid, ))
    CONN.commit()

def no_customers():
    sql = """    
        SELECT count(1) FROM customers
    """
    customer_count = CURSOR.execute(sql).fetchall()
    if customer_count !=0:
        return False
    else:
        return True

def customer_create():
    customers = Customer.get_table_rows()
    ap_firstname = input("Ονομα: ")
    ap_lastname = input("Επωνυμο: ")
    ap_mobile = input("Κινητο : ")
    ap_email = input("Email: ")
    newcustomer=Customer.create(ap_firstname,ap_lastname,ap_mobile,ap_email)
    print(newcustomer)
    customers.append(newcustomer)

def customer_modify():
    customers = Customer.get_table_rows()
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
    customers = Customer.get_table_rows()
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
            tmpcustomer=customers[customerIDs[choice]]
            print(tmpcustomer)

            delete_appointments_of_customerid(choice)

            tmpcustomer.delete()
            customers.pop(customerIDs[choice])

        elif choice == 99:
            break
        else:
            print("Λαθος επιλογη. Παρακαλω επιλεξτε παλι.")