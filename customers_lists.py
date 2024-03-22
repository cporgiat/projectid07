customers = []

class Customer():
    '''Η κλάση Customer περιγράφει έναν πελατη και την μέθοδο __str__.'''
    def __init__(self, ap_firstname, ap_lastname, ap_mobile, ap_email, ap_customerID=0):
        self.firstname=ap_firstname
        self.lastname=ap_lastname
        self.mobile=ap_mobile
        self.email=ap_email
        self.customerID=ap_customerID

    def changeFirstName(self, ap_firstname):
        self.firstname=ap_firstname

    def changeLastName(self, ap_lastname):
        self.lastname=ap_lastname

    def changeMobile(self, ap_mobile):
        self.mobile=ap_mobile

    def changeEmail(self, ap_email):
        self.email=ap_email

    def __str__(self):
        return "ID: "+str(self.customerID)+" Ονομα: "+self.firstname+" Επωνυμο: "+self.lastname+" Κινητο: "+str(self.mobile)+" Email: "+self.email

class Appointment():
    '''Η κλάση Customer περιγράφει έναν πελατη και την μέθοδο __str__.'''
    def __init__(self, ap_customerID, ap_date, ap_time, ap_duration=20):
        self.customerID=ap_customerID
        self.date=ap_date
        self.time=ap_time
        self.duration=ap_duration

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
            customer_create()
        elif choice == '2':
            customer_modify()
        elif choice == '3':
            customer_delete()
        elif choice == '99':
            break
        else:
            print("Λαθος επιλογη. Παρακαλω επιλεξτε παλι.")

def customer_create():
    global customers
    nc_firstname = input("Ονομα: ")
    nc_lastname = input("Επωνυμο: ")
    nc_mobile = input("Κινητο : ")
    nc_email = input("Email: ")
    newcustomer=Customer(nc_firstname,nc_lastname,nc_mobile,nc_email)
    print(newcustomer)
    customers.append(newcustomer)

def customer_modify():
    global customers
    customerIDs = {}
    counter = 0
    for customer in customers:
        customerIDs[customer.customerID]=counter
        counter=counter+1

    while True:
        for customer in customers:
            print(customer)
        choice = int(input("Επιλεξτε το ID του πελατη που θελετε να τροποποιησετε η 99 για επιστροφη: "))

        if choice in customerIDs:
            print("Επιλεξατε τον πελατη: ")
            tmp=customers[customerIDs[choice]]
            print(tmp)

            while True:
                print("1. Αλλαγη Ονοματος")
                print("2. Αλλαγη Επωνυμου")
                print("3. Αλλαγη Κινητου")
                print("4. Αλλαγη Email")
                print("99. Προηγουμενο menu")

                choice = input("Επιλεξτε αλλαγη: ")

                if choice == '1':
                    tempinput = input("Νεο ονομα: ")
                    tmp.changeFirstName(tempinput)
                    print(tmp)
                elif choice == '2':
                    tempinput = input("Νεο Επωνυμο: ")
                    tmp.changeLastName(tempinput)
                    print(tmp)
                elif choice == '3':
                    tempinput = input("Νεο Κινητο: ")
                    tmp.changeMobile(tempinput)
                    print(tmp)
                elif choice == '4':
                    tempinput = input("Νεο Email: ")
                    tmp.changeEmail(tempinput)
                    print(tmp)
                elif choice == '99':
                    break
                else:
                    print("Λαθος επιλογη. Παρακαλω επιλεξτε παλι.")
        elif choice == 99:
            break
        else:
            print("Λαθος επιλογη. Παρακαλω επιλεξτε παλι.")

def customer_delete():
    global customers
    customerIDs = {}
    counter = 0
    for customer in customers:
        customerIDs[customer.customerID] = counter
        counter = counter + 1

    while True:
        if len(customers) == 0:
            print("Δεν υπαρχουν πελατες. Επιστροφη στο προηγουμενο μενου.")
            break
        for customer in customers:
            print(customer)
        choice = int(input("Επιλεξτε το ID του πελατη που θελετε να διαγραψετε η 99 για επιστροφη: "))

        if choice in customerIDs:
            print("Διαγραψατε τον πελατη: ")
            tmp=customers[customerIDs[choice]]
            print(tmp)
            customers.pop(customerIDs[choice])
        elif choice == 99:
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