import sqlite3
import pandas as pd

# Δημιουργία σύνδεσης με τη βάση δεδομένων SQLite
conn = sqlite3.connect('appointments.db')
cursor = conn.cursor()


# Αναζήτηση με βάση την ημερομηνία
def search_by_date(date):
    sql = """
        SELECT app.id, cust.firstname, cust.lastname, app.datetime, app.duration 
        FROM appointments app
        LEFT JOIN customers cust ON app.customerid = cust.id
        WHERE app.datetime LIKE ?
    """
    # Χρησιμοποιώντας το LIKE για αναζήτηση ημερομηνίας
    results = cursor.execute(sql, (f"%{date}%",)).fetchall()
    return results


# Αναζήτηση με βάση το όνομα πελάτη
def search_by_customer_name(name):
    sql = """
        SELECT app.id, cust.firstname, cust.lastname, app.datetime, app.duration 
        FROM appointments app
        LEFT JOIN customers cust ON app.customerid = cust.id
        WHERE cust.firstname LIKE ? OR cust.lastname LIKE ?
    """
    results = cursor.execute(sql, (f"%{name}%", f"%{name}%",)).fetchall()
    return results


# Εξαγωγή των αποτελεσμάτων σε αρχείο Excel
def export_to_excel(data, filename):
    # Δημιουργία DataFrame από τα δεδομένα
    df = pd.DataFrame(data, columns=["ID", "Firstname", "Lastname", "Datetime", "Duration"])

    # Εξαγωγή σε Excel
    df.to_excel(filename, index=False, engine='xlsxwriter')
    print(f"Τα δεδομένα εξήχθησαν στο αρχείο {filename}.")


# Ερώτηση για αναζήτηση με ημερομηνία ή με όνομα πελάτη
search_type = input("Επιλέξτε τύπο αναζήτησης (1 για ημερομηνία, 2 για όνομα πελάτη): ")

if search_type == "1":
    date_input = input("Εισάγετε την ημερομηνία (YYYY-MM-DD): ")
    results = search_by_date(date_input)
elif search_type == "2":
    name_input = input("Εισάγετε το όνομα του πελάτη: ")
    results = search_by_customer_name(name_input)
else:
    results = []
    print("Άκυρη επιλογή.")

# Εμφάνιση αποτελεσμάτων
if results:
    print("Αποτελέσματα αναζήτησης:")
    for row in results:
        print(row)

    # Ερώτηση για εξαγωγή σε Excel
    export_excel = input("Θέλετε να εξάγετε τα αποτελέσματα σε Excel; (ναι/όχι): ")

    if export_excel.lower() == "ναι":
        filename = input("Εισάγετε το όνομα του αρχείου (π.χ., results.xlsx): ")
        export_to_excel(results, filename)
else:
    print("Δεν βρέθηκαν αποτελέσματα.")
