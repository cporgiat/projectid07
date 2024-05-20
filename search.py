import sqlite3
import pandas as pd


# Σύνδεση με τη βάση δεδομένων
def get_connection():
    return sqlite3.connect('appointments.db')


# Συνάρτηση αναζήτησης με βάση την ημερομηνία
def search_by_date(date):
    with get_connection() as conn:
        cursor = conn.cursor()
        sql = """
            SELECT app.id, cust.firstname, cust.lastname, app.datetime, app.duration, cust.email
            FROM appointments app
            JOIN customers cust ON app.customerid = cust.id
            WHERE DATE(app.datetime) = ?
        """
        results = cursor.execute(sql, (date,)).fetchall()
    return results


# Συνάρτηση αναζήτησης με βάση το email πελάτη
def search_by_customer_email(email):
    with get_connection() as conn:
        cursor = conn.cursor()
        sql = """
            SELECT app.id, cust.firstname, cust.lastname, app.datetime, app.duration, cust.email
            FROM appointments app
            JOIN customers cust ON app.customerid = cust.id
            WHERE cust.email = ?
        """
        results = cursor.execute(sql, (email,)).fetchall()
    return results

# Συνάρτηση για εκτύπωση αποτελεσμάτων στην οθόνη
def print_results(results):
    for result in results:
        print(f"ID: {result[0]}, Πελάτης: {result[1]} {result[2]}, Ημερομηνία: {result[3]}, Διάρκεια: {result[4]} λεπτά, Email: {result[5]}")


# Συνάρτηση για εξαγωγή σε Excel
def export_to_excel(results, filename):
    df = pd.DataFrame(results, columns=['ID', 'First Name', 'Last Name', 'Datetime', 'Duration', 'Email'])
    df.to_excel(filename, index=False)
    print(f"Εξαγωγή σε Excel με όνομα {filename}")
