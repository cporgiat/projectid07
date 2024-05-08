from search import (
    search_by_date,
    search_by_customer_name,
    print_results,
    export_to_excel
)


def search_menu():
    while True:
        print("\n--- Μενού Αναζήτησης ---")
        print("1. Αναζήτηση με βάση την ημερομηνία")
        print("2. Αναζήτηση με βάση το όνομα του πελάτη")
        print("99. Επιστροφη στο προηγουμενο Menu")

        choice = input("Επιλέξτε μια επιλογή: ")

        if choice == "1":
            # Αναζήτηση με βάση την ημερομηνία
            date = input("Εισάγετε την ημερομηνία (YYYY-MM-DD): ")
            results = search_by_date(date)
            if results:
                print_results(results)  # Εκτύπωση των αποτελεσμάτων
                export_choice = input("Θέλετε να εξαγάγετε σε Excel; (ναι/όχι): ")
                if export_choice.lower() == "ναι":
                    filename = input("Πληκτρολογήστε το όνομα του αρχείου Excel (χωρίς κατάληξη): ")
                    export_to_excel(results, filename + ".xlsx")
            else:
                print("Δεν βρέθηκαν αποτελέσματα.")

        elif choice == "2":
            # Αναζήτηση με βάση το όνομα του πελάτη
            firstname = input("Εισάγετε το όνομα του πελάτη: ")
            lastname = input("Εισάγετε το επώνυμο του πελάτη: ")
            results = search_by_customer_name(firstname, lastname)
            if results:
                print_results(results)  # Εκτύπωση των αποτελεσμάτων
                export_choice = input("Θέλετε να εξαγάγετε σε Excel; (ναι/όχι): ")
                if export_choice.lower() == "ναι":
                    filename = input("Πληκτρολογήστε το όνομα του αρχείου Excel (χωρίς κατάληξη): ")
                    export_to_excel(results, filename + ".xlsx")
            else:
                print("Δεν βρέθηκαν αποτελέσματα.")

        elif choice == "99":
            break  # Τερματίζουμε τον βρόχο

        else:
            print("Μη έγκυρη επιλογή, παρακαλώ δοκιμάστε ξανά.")


# Εκτελούμε το menu αν το αρχείο εκτελείται άμεσα
if __name__ == "__main__":
    search_menu()
