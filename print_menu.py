from print import (
    print_customer_by_name,
    print_appointments_by_date,
    print_appointments_in_range
)

# Συνάρτηση που διαχειρίζεται το μενού εκτύπωσης
def print_menu():
    while True:
        print("\n--- Μενού Εκτύπωσης ---")
        print("1. Εκτύπωση πελάτη με βάση το όνομα και το επώνυμο")
        print("2. Εκτύπωση ραντεβού με βάση ημερομηνία")
        print("3. Εκτύπωση ραντεβού σε εύρος ημερομηνιών")
        print("99. Έξοδος από το μενού")

        choice = input("Επιλέξτε μια επιλογή: ")

        # Εάν η επιλογή είναι για έξοδο, τερματίζουμε τον βρόχο χωρίς επιπλέον ερωτήσεις
        if choice == "99":
            print("Έξοδος από το μενού εκτύπωσης.")
            break  # Τερματίζουμε το while loop

        # Ρωτάμε για εκτύπωση μόνο αν δεν πρόκειται για έξοδο
        use_printer_input = input("Θέλετε να εκτυπώσετε σε εκτυπωτή ή στην οθόνη; (εκτυπωτής/οθόνη): ")
        use_printer = True if use_printer_input.lower() == "εκτυπωτής" else False

        if choice == "1":
            firstname = input("Εισάγετε το όνομα του πελάτη: ")
            lastname = input("Εισάγετε το επώνυμο του πελάτη: ")
            print_customer_by_name(firstname, lastname, use_printer)

        elif choice == "2":
            date = input("Εισάγετε την ημερομηνία (YYYY-MM-DD): ")
            print_appointments_by_date(date, use_printer)

        elif choice == "3":
            start_date = input("Εισάγετε την αρχική ημερομηνία (YYYY-MM-DD): ")
            end_date = input("Εισάγετε την τελική ημερομηνία (YYYY-MM-DD): ")
            print_appointments_in_range(start_date, end_date, use_printer)

        else:
            print("Μη έγκυρη επιλογή, παρακαλώ δοκιμάστε ξανά.")


# Εκτέλεση του μενού εκτύπωσης όταν το αρχείο τρέχει απευθείας
if __name__ == "__main__":
    print_menu()
