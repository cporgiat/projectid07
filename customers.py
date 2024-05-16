import sqlite3


def create_table():
    """ Creates the customers table if it does not already exist"""
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
    """ Drops the customers table if it does already exist"""
    sql = """   
        DROP TABLE IF EXISTS customers;
    """
    CURSOR.execute(sql)
    CONN.commit()


# sqlite3 has a connect() method which accepts a .db file as a destination
CONN = sqlite3.connect('appointments.db')

# once we establish our connection and assign it to CONN, we create a CURSOR
CURSOR = CONN.cursor()

# Customer.drop_table() # Only use this to reinitialize the table
create_table()


class Customer:
    """ This class describes a customer and handles all needed operations so that changes to a customer are stored
    in the database in the form of a database table called customers """
    def __init__(self, ap_firstname, ap_lastname, ap_mobile, ap_email):
        self.firstname = ap_firstname
        self.lastname = ap_lastname
        self.mobile = ap_mobile
        self.email = ap_email

    def save(self):
        """ This method saves a Customer object to customers table in the form of columns.
        Each class attribute is mapped to a table column (e.g. Customer.firstname -> customers.firstname)
        and assigns a unique number to the row inserted, by getting the last assigned id number
        using attribute lastrowid of cursor() method"""
        sql = """
            INSERT INTO customers (firstname, lastname, mobile, email)
            VALUES (?, ?, ?, ?)
        """
        CURSOR.execute(sql, (self.firstname, self.lastname, self.mobile, self.email))
        CONN.commit()

        self.id = CURSOR.lastrowid

    def update(self):
        """ This method updates customers table columns with the attributes of a Customer object as
        identified by its unique ID number (costomers.id column).
        Each class attribute is mapped to a table column (e.g. Customer.firstname -> customers.firstname) """
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
        """ This method deletes customers table the row that belongs to Customer object as
        identified by its unique ID number (costomers.id column). """
        sql = """
            delete from customers 
            WHERE id=?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

    @classmethod
    def create(cls, firstname, lastname, mobile, email):
        """ This class method creates a new instance of Customer and saves it to the database using save() method
        and returns the newly created Customer object"""
        new_instance = cls(firstname, lastname, mobile, email)
        new_instance.save()

        return new_instance

    @classmethod
    def create_from_db(cls, table_row):
        """ This class method creates a new instance of Customer from its associated row in the database
        and returns the newly created Customer object"""
        new_instance = cls(table_row[1], table_row[2], table_row[3], table_row[4])
        new_instance.id = table_row[0]

        return new_instance

    @classmethod
    def get_table_rows(cls):
        """ This class method returns all rows of the customer table on the database and creates
        the Customer objects as described by each row and returns the rows of customers tables
        in the form of a list of tuples """
        sql = """    
            SELECT * FROM customers
        """
        table_rows = CURSOR.execute(sql).fetchall()

        return [cls.create_from_db(row) for row in table_rows]

    def change_firstname(self, ap_firstname):
        """ This method changes the firstname attribute of a Customer object and updates its
        associated row on the customers table """
        self.firstname = ap_firstname
        self.update()

    def change_lastname(self, ap_lastname):
        """ This method changes the lastname attribute of a Customer object and updates its
        associated row on the customers table """
        self.lastname = ap_lastname
        self.update()

    def change_mobile(self, ap_mobile):
        """ This method changes the mobile attribute of a Customer object and updates its
        associated row on the customers table """
        self.mobile = ap_mobile
        self.update()

    def change_email(self, ap_email):
        """ This method changes the email attribute of a Customer object and updates its
        associated row on the customers table """
        self.email = ap_email
        self.update()

    def __str__(self):
        return "ID: " + str(self.id) + " Ονομα: " + self.firstname + " Επωνυμο: " + self.lastname + " Κινητο: " + str(
            self.mobile) + " Email: " + self.email


def no_customers():
    """ This method counts the number of rows of the customers table """
    sql = """    
        SELECT count(1) FROM customers
    """
    customer_count_tuple = CURSOR.execute(sql).fetchone()
    customer_count = int(customer_count_tuple[0])
    if customer_count != 0:
        return False
    else:
        return True


def get_customer_fullname_by_id(ap_customerid):
    """ This method returns a tuple with the fullname (firstname lastname) of a customer as identified by its ID """
    sql = """    
        SELECT firstname+" "+lastname FROM customers where id= ?
    """
    return CURSOR.execute(sql, (ap_customerid,)).fetchall()


def get_customer_id_by_email(ap_customeremail):
    """ This method returns a tuple with the ID of the customers that their email are matching the input"""
    sql = """    
        SELECT id FROM customers where email like '%?%'
    """
    return CURSOR.execute(sql, (ap_customeremail,)).fetchall()


def get_customer_id_by_phone(ap_customerphone):
    """ This method returns a tuple with the ID of the customers that their phone are matching the input"""
    sql = """    
        SELECT id FROM customers where phone like '%?%'
    """
    return CURSOR.execute(sql, (ap_customerphone,)).fetchall()


def delete_appointments_of_customerid(ap_customerid):
    """ This method deletes all the appointments of a customer as identified by its ID"""
    sql = """
        delete from appointments 
        WHERE customerid=?
    """
    CURSOR.execute(sql, (ap_customerid,))
    CONN.commit()

