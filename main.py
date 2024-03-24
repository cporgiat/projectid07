import appointments
import customers

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
            customers.customer_create()
        elif choice == '2':
            customers.customer_modify()
        elif choice == '3':
            customers.customer_delete()
        elif choice == '99':
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
            appointments.appointment_create()
        elif choice == '2':
            appointments.appointment_modify()
        elif choice == '3':
            appointments.appointment_delete()
        elif choice == '99':
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

    menu_main()
