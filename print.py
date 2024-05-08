import win32print
import win32api
import os
import sqlite3
from search import get_connection  # Αν χρειάζεστε σύνδεση με τη βάση δεδομένων


# Συνάρτηση για εκτύπωση σε εκτυπωτή ή οθόνη
def print_or_send_to_printer(content, use_printer=False):
    if use_printer:
        # Δημιουργούμε ένα προσωρινό αρχείο με το περιεχόμενο
        temp_filename = "temp_print.txt"
        with open(temp_filename, "w") as f:
            f.write(content)

        # Αποστέλλουμε το προσωρινό αρχείο στον προεπιλεγμένο εκτυπωτή στα Windows
        printer_name = win32print.GetDefaultPrinter()  # Προεπιλεγμένος εκτυπωτής
        win32api.ShellExecute(0, "print", temp_filename, f'/d:"{printer_name}"', ".", 0)

        print("Το περιεχόμενο στάλθηκε στον εκτυπωτή.")

        # Διαγράφουμε το προσωρινό αρχείο
        os.remove(temp_filename)
    else:
        # Εκτύπωση στην οθόνη
        print(content)

# Συνάρτηση για εκτύπωση πελάτη με βάση το όνομα και το επώνυμο
def print_customer_by_name(firstname, lastname, use_printer=False):
    content = ""
    with get_connection() as conn:
        cursor = conn.cursor()
        sql = """
            SELECT id, firstname, lastname, mobile, email
            FROM customers
            WHERE firstname = ? AND lastname = ?
        """
        customer = cursor.execute(sql, (firstname, lastname)).fetchone()

        if customer:
            content += f"ID: {customer[0]}\n"
            content += f"Όνομα: {customer[1]}\n"
            content += f"Επώνυμο: {customer[2]}\n"
            content += f"Κινητό: {customer[3]}\n"
            content += f"Email: {customer[4]}\n"
        else:
            content += "Ο πελάτης δεν βρέθηκε.\n"

    # Εκτύπωση με τη συνάρτηση που επιλέγει οθόνη ή εκτυπωτή
    print_or_send_to_printer(content, use_printer)


# Συνάρτηση για εκτύπωση ραντεβού με βάση ημερομηνία
def print_appointments_by_date(date, use_printer=False):
    content = ""
    with get_connection() as conn:
        cursor = conn.cursor()
        sql = """
            SELECT app.id, app.datetime, app.duration, cust.firstname, cust.lastname
            FROM appointments app
            JOIN customers cust ON app.customerid = cust.id
            WHERE DATE(app.datetime) = ?
        """
        appointments = cursor.execute(sql, (date,)).fetchall()

        if appointments:
            content += f"Ραντεβού για την ημερομηνία {date}:\n"
            for app in appointments:
                content += f"ID: {app[0]}, Πελάτης: {app[3]} {app[4]}, Ημερομηνία: {app[1]}, Διάρκεια: {app[2]} λεπτά\n"
        else:
            content += "Δεν βρέθηκαν ραντεβού για αυτήν την ημερομηνία.\n"

    # Εκτύπωση με τη συνάρτηση που επιλέγει οθόνη ή εκτυπωτή
    print_or_send_to_printer(content, use_printer)


# Συνάρτηση για εκτύπωση ραντεβού με βάση εύρος ημερομηνιών
def print_appointments_in_range(start_date, end_date, use_printer=False):
    content = ""
    with get_connection() as conn:
        cursor = conn.cursor()
        sql = """
            SELECT app.id, app.datetime, app.duration, cust.firstname, cust.lastname
            FROM appointments app
            JOIN customers cust ON app.customerid = cust.id
            WHERE DATE(app.datetime) BETWEEN ? AND ?
        """
        appointments = cursor.execute(sql, (start_date, end_date)).fetchall()

        if appointments:
            content += f"Ραντεβού από {start_date} έως {end_date}:\n"
            for app in appointments:
                content += f"ID: {app[0]}, Πελάτης: {app[3]} {app[4]}, Ημερομηνία: {app[1]}, Διάρκεια: {app[2]} λεπτά\n"
        else:
            content += "Δεν βρέθηκαν ραντεβού σε αυτό το εύρος ημερομηνιών.\n"

    # Εκτύπωση με τη συνάρτηση που επιλέγει οθόνη ή εκτυπωτή
    print_or_send_to_printer(content, use_printer)
