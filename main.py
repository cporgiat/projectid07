import appointments_menu
import customers_menu
import search_menu


def menu_main():
    while True:
        print("")
        print("Κεντρικο Menu:")
        print("1. Διαχειρηση πελατων")
        print("2. Διαχειρηση ραντεβου")
        print("3. Αναζητηση")
        print("4. Υπενθυμιση")
        print("5. Εκτυπωση")
        print("98. Ρυθμισεις εφαρμογης")
        print("99. Εξοδος προγραμματος")

        choice = input("Επιλογη: ")

        if choice == '1':
            customers_menu.menu_customer()
        elif choice == '2':
            appointments_menu.menu_appointment()
        elif choice == '3':
            search_menu.menu_search()
        elif choice == '4':
            mail_menu.menu_mail()
        elif choice == '5':
            printout_menu.menu_printout()
        elif choice == '98':
            settings_menu.menu_settings()
        elif choice == '99':
            print("Εξοδος απο το προγραμμα")
            break
        else:
            print("Λαθος επιλογη. Παρακαλω επιλεξτε παλι.")


if __name__ == '__main__':
    menu_main()
