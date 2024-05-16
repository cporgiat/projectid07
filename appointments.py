import sqlite3


def create_table():
    """ Creates the appointments table if it does not already exist"""
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
    """ Drops the appointments table if it does already exist"""
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
    """ This class describes an appointment and handles all needed operations so that changes to
    an appointment are stored in the database in the form of a database table called appointments.
    Note that customer information is normalized, and only the ID of the associated customer is
    assigned to each Appointment object in the customerid attribute"""

    def __init__(self, ap_customerid, ap_datetime, ap_duration=20):
        self.customerid = ap_customerid
        self.datetime = ap_datetime
        self.duration = ap_duration

    def save(self):
        """ This method saves an Appointment object to appointments table in the form of columns.
        Each class attribute is mapped to a table column (e.g. Appointment.datetime -> appointments.datetime)
        and assigns a unique number to the row inserted, by getting the last assigned id number
        using attribute lastrowid of cursor() method"""
        sql = """
            INSERT INTO appointments (customerid, datetime, duration)
            VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (self.customerid, self.datetime, self.duration))
        CONN.commit()

        self.id = CURSOR.lastrowid

    def update(self):
        """ This method updates appointments table columns with the attributes of an Appointment object as
        identified by its unique ID number (appointments.id column).
        Each class attribute is mapped to a table column (e.g. Appointment.datetime -> appointments.datetime) """
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
        """ This method deletes from appointments table the row that belongs to Appointment object as
        identified by its unique ID number (appointments.id column). """
        sql = """
            delete from appointments 
            WHERE id=?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

    @classmethod
    def create(cls, ap_customerid, ap_datetime, ap_duration):
        """ This class method creates a new instance of Appointment and saves it to the database using save() method
        and returns the newly created Appointment object"""
        new_instance = cls(ap_customerid, ap_datetime, ap_duration)
        new_instance.save()

        return new_instance

    @classmethod
    def create_from_db(cls, table_row):
        """ This class method creates a new instance of Appointment from its associated row in the database
        and returns the newly created Appointment object"""
        new_instance = cls(table_row[1], table_row[2], table_row[3])
        new_instance.id = table_row[0]

        return new_instance

    @classmethod
    def get_table_rows(cls):
        """ This class method returns all rows of the appointments table on the database and creates
        the Appointment objects as described by each row and returns the rows of appointments tables
        in the form of a list of tuples """
        sql = """    
            SELECT * FROM appointments
        """
        table_rows = CURSOR.execute(sql).fetchall()

        return [cls.create_from_db(row) for row in table_rows]

    def change_customerid(self, ap_customerid):
        """ This method changes the customerid attribute of an Appointment object and updates its
        associated row on the appointments table """
        self.customerid = ap_customerid
        self.update()

    def change_datetime(self, ap_datetime):
        """ This method changes the datetime attribute of an Appointment object and updates its
        associated row on the appointments table """
        self.datetime = ap_datetime
        self.update()

    def change_duration(self, ap_duration):
        """ This method changes the duration attribute of an Appointment object and updates its
        associated row on the appointments table """
        self.duration = ap_duration
        self.update()

    def __str__(self):
        return "ID: " + str(self.id) + " customerID: " + str(
            self.customerid) + " Ημερομηνια: " + self.datetime + " Διαρκεια: " + str(self.duration)


def list_appointments_with_customer_fullname():
    """ This method returns tuples with the appointments and literal firstname lastname of a customer
    as identified by its ID """
    sql = """
        select app.id,cust.firstname,cust.lastname,app.datetime,app.duration from appointments app
        left join customers cust on app.customerid=cust.id
    """
    table_rows = CURSOR.execute(sql).fetchall()
    return table_rows


def appointment_by_id_with_customer_fullname(ap_appointmentid):
    """ This method returns a tuple of an appointment matching the input ID and literal firstname lastname of a customer
    as identified by its ID """
    sql = """
        select app.id,cust.firstname,cust.lastname,app.datetime,app.duration from appointments app
        join customers cust on app.customerid=cust.id
        where app.id = ?
    """
    return CURSOR.execute(sql, (ap_appointmentid,)).fetchone()


def appointment_search_bydate():
    """ Placeholder """
    appointments_list = Appointment.get_table_rows()


def appointment_search_bycustomerid():
    """ Placeholder """
    appointments_list = Appointment.get_table_rows()


def no_appointments():
    """ This method counts the number of rows in the appointments table and returns True it the count is 0"""
    sql = """    
        SELECT count(1) FROM appointments
    """
    apointment_count_tuple = CURSOR.execute(sql).fetchone()
    appointment_count = int(apointment_count_tuple[0])
    if appointment_count != 0:
        return False
    else:
        return True


def no_overlapping_appointments(ap_datetime, ap_duration):
    """ This method checks if the input date time and duration is overlapping with existing appointments
    by counting the results of the query below, and returns True if the count is 0
    Note: The query returns the ids of all the appointments that have a start datetime less than or equal to the input
    and have an end datetime (datetime+duration) greater or equal to the input
    AND (union)
    the ids of all the appointments that have a start datetime greater than or equal to the input and have an end
    datetime (datetime+duration) greater or equal to the input.
    If both queries return no ids, that means that no appointment exists that includes the input time range
    with start of datetime and end of datetime+duration"""
    sql = """
        with ids as (
            select id FROM appointments app 
                where datetime(app.datetime) <= datetime( ? )
                and datetime(app.datetime,'+'||app.duration||' minutes') >= datetime( ? )
            union
            select id FROM appointments app 
                where datetime(app.datetime) <= datetime( ? ,'+'||?||' minutes')
                and datetime(app.datetime,'+'||app.duration||' minutes') >= datetime( ? ,'+'||?||' minutes')
        )
        select count(1) from ids
    """
    overlapping_appointments_count_tuple = CURSOR.execute(sql, (ap_datetime, ap_datetime, ap_datetime, ap_duration, ap_datetime, ap_duration)).fetchone()
    overlapping_appointments_count = int(overlapping_appointments_count_tuple[0])

    if overlapping_appointments_count != 0:
        return False
    else:
        return True
