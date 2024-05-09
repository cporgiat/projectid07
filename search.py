from tkinter import *

def create_search_widget(parent):
    search_widget = Frame(parent)
    
    label1 = Label(search_widget, text="Αναζήτηση")
    label1.grid(row=0, column=0)

    entry = Entry(search_widget, width=30)
    entry.grid(row=0, column=1)

    def search():
        search_term = entry.get()  # Get the text entered in the entry widget
        # Perform the search operation using the search term (you can replace this with your actual search logic)
        print("Searching for:", search_term)

    button = Button(search_widget, text="Search", command=search)
    button.grid(row=0, column=2, pady=10)

    return search_widget, entry, button
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
            SELECT app.id, cust.firstname, cust.lastname, app.datetime, app.duration
            FROM appointments app
            JOIN customers cust ON app.customerid = cust.id
            WHERE DATE(app.datetime) = ?
        """
        results = cursor.execute(sql, (date,)).fetchall()
    return results


# Συνάρτηση αναζήτησης με βάση το όνομα πελάτη
def search_by_customer_name(firstname, lastname):
    with get_connection() as conn:
        cursor = conn.cursor()
        sql = """
            SELECT app.id, cust.firstname, cust.lastname, app.datetime, app.duration
            FROM appointments app
            JOIN customers cust ON app.customerid = cust.id
            WHERE cust.firstname = ? AND cust.lastname = ?
        """
        results = cursor.execute(sql, (firstname, lastname)).fetchall()
    return results


# Συνάρτηση για εκτύπωση αποτελεσμάτων στην οθόνη
def print_results(results):
    for result in results:
        print(f"ID: {result[0]}, Πελάτης: {result[1]} {result[2]}, Ημερομηνία: {result[3]}, Διάρκεια: {result[4]} λεπτά")


# Συνάρτηση για εξαγωγή σε Excel
def export_to_excel(results, filename):
    df = pd.DataFrame(results, columns=['ID', 'First Name', 'Last Name', 'Datetime', 'Duration'])
    df.to_excel(filename, index=False)
    print(f"Εξαγωγή σε Excel με όνομα {filename}")
