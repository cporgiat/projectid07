


def menu_search():
    while True:
        print("")
        print("Επιλέξτε τύπο αναζήτησης")
        print("1. Αναζητηση με Ημερομηνια")
        print("2. Αναζητηση με Ονομα Πελατη")
        print("99. Προηγουμενο menu")

        choice = input("Επιλογη: ")

        if choice == '1':
            search.search_by_date()
        elif choice == '2':
            search.search_by_customer_name()
        elif choice == '99':
            break
        else:
            print("Λαθος επιλογη. Παρακαλω επιλεξτε παλι.")
