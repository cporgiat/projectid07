import sqlite3


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


def appointment_search_bydate():
    appointments_list = Appointment.get_table_rows()


def appointment_search_bycustomerid():
    appointments_list = Appointment.get_table_rows()


def no_appointments():
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
