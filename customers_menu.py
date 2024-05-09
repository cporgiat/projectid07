import customers
import utils


def menu_customer():
    while True:
        print("")
        print("Διαχειρηση πελατων:")
        print("1. Δημιουργεια πελατη")
        print("2. Τροποποιηση πελατη")
        print("3. Διαγραφη πελατη")
        print("99. Προηγουμενο menu")

        choice = utils.get_number("Επιλογη: ")

        if choice == '1':
            menu_customer_create()
        elif choice == '2':
            menu_customer_modify()
        elif choice == '3':
            menu_customer_delete()
        elif choice == '99':
            break
        else:
            print("Λαθος επιλογη. Παρακαλω επιλεξτε παλι.")


def menu_customer_create():
    ap_firstname = utils.get_name("Ονομα: ")
    ap_lastname = utils.get_name("Επωνυμο: ")
    ap_mobile = utils.get_number("Κινητο : ")
    ap_email = utils.get_email("Email: ")
    newcustomer = customers.Customer.create(ap_firstname, ap_lastname, ap_mobile, ap_email)
    print(newcustomer)


def menu_customer_modify():
    if customers.no_customers():
        print("Δεν υπαρχουν πελατες. Επιστροφη στο προηγουμενο μενου.")
        return

    customers_list = customers.Customer.get_table_rows()
    customerIDs = {}
    counter = 0
    for customer in customers_list:
        customerIDs[customer.id] = counter
        counter = counter + 1

    while True:
        print("")
        print("Λιστα πελατων:")
        for customer in customers_list:
            print(customer)
        choice = int(utils.get_number("Επιλεξτε το ID του πελατη που θελετε να τροποποιησετε η 99 για επιστροφη: "))

        if choice in customerIDs:
            print("Επιλεξατε τον πελατη: ")
            tmp = customers_list[customerIDs[choice]]
            print(tmp)

            while True:
                print("1. Αλλαγη Ονοματος")
                print("2. Αλλαγη Επωνυμου")
                print("3. Αλλαγη Κινητου")
                print("4. Αλλαγη Email")
                print("99. Προηγουμενο menu")

                choice = utils.get_number("Επιλεξτε αλλαγη: ")

                if choice == '1':
                    tempinput = utils.get_name("Νεο ονομα: ")
                    tmp.change_firstname(tempinput)
                    print("")
                    print(tmp)
                elif choice == '2':
                    tempinput = utils.get_name("Νεο Επωνυμο: ")
                    tmp.change_lastname(tempinput)
                    print("")
                    print(tmp)
                elif choice == '3':
                    tempinput = utils.get_number("Νεο Κινητο: ")
                    tmp.change_mobile(tempinput)
                    print("")
                    print(tmp)
                elif choice == '4':
                    tempinput = utils.get_email("Νεο Email: ")
                    tmp.change_email(tempinput)
                    print("")
                    print(tmp)
                elif choice == '99':
                    break
                else:
                    print("Λαθος επιλογη. Παρακαλω επιλεξτε παλι.")
        elif choice == 99:
            break
        else:
            print("Λαθος επιλογη. Παρακαλω επιλεξτε παλι.")


def menu_customer_delete():
    if customers.no_customers():
        print("Δεν υπαρχουν πελατες. Επιστροφη στο προηγουμενο μενου.")
        return

    customers_list = customers.Customer.get_table_rows()
    customerIDs = {}
    counter = 0
    for customer in customers_list:
        customerIDs[customer.id] = counter
        counter = counter + 1

    while True:
        if customers.no_customers():
            print("Δεν υπαρχουν πελατες. Επιστροφη στο προηγουμενο μενου.")
            break
        print("")
        print("Λιστα πελατων:")
        for customer in customers_list:
            print(customer)
        choice = int(utils.get_number("Επιλεξτε το ID του πελατη που θελετε να διαγραψετε η 99 για επιστροφη: "))

        if choice in customerIDs:
            print("Διαγραψατε τον πελατη: ")
            tmpcustomer = customers_list[customerIDs[choice]]
            print(tmpcustomer)

            customers.delete_appointments_of_customerid(choice)

            tmpcustomer.delete()
            customers_list.pop(customerIDs[choice])

        elif choice == 99:
            break
        else:
            print("Λαθος επιλογη. Παρακαλω επιλεξτε παλι.")
