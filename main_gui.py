if __name__ == '__main__':
    import customtkinter
    import tkinter as tk
    from datetime import datetime
    from tkcalendar import DateEntry
    from search import search_by_date, search_by_customer_email, export_to_excel
    from tkinter import messagebox, ttk
    from reminder import send_reminder     
    from customers import Customer, no_customers, delete_appointments_of_customerid
    from utils import validate_input_email, validate_input_only_letters, validate_input_only_numbers
    from appointments import Appointment, no_overlapping_appointments, no_appointments, list_appointments_with_customer_fullname, Appointment

#Κάνουμε import τα libraries και τα functions που θα χρησιμοποιηθούν από τα άλλα αρχεία 

    def load_logo(scale_factor=0.5):
    #function για το logo μέσα στο πρόγραμμα
        try:
            logo = tk.PhotoImage(file="assets/logo.png")
            logo = logo.subsample(int(1.5 / scale_factor))  # Κλιμάκωση του λογότυπου
            return logo
        # Βρίσκει την εικόνα ,την κάνει widget και την κάνει resize στο σωστό μέγεθος 
        except tk.TclError as e:
        # Σε περιπτώση σφάλματος εμφανίζει error
            messagebox.showerror("Error", f"Failed to load logo: {e}")
            return None


    def clear_content_frame(frame):
        #Βρίσκει και διαγράφει όλα τα widgets μέσα στο frame που καλούμε
        for widget in frame.winfo_children():
            widget.destroy()

# funcion για να φτιάξεις νέο πελάτη
    def new_customer_clicked(event=None):
        #Καθαρίζει τα παλιά widgets του frame
        clear_content_frame(content_frame)
        
        def retrieve_input():
            ap_firstname = textbox_firstname.get("1.0", "end-1c")
            ap_lastname = textbox_lastname.get("1.0", "end-1c")
            ap_mobile = textbox_phone.get("1.0", "end-1c")
            ap_email = textbox_email.get("1.0", "end-1c")
            #παίρνω τα δεδομένα από τα πεδία

            if (not validate_input_only_letters(ap_firstname)):
                tk.messagebox.showerror("Λαθος Εισοδος", "Παρακαλω για το όνομα χρησιμοποιήστε μόνο\n "
                                                         "Ελληνικους η Λατινικους χαρακτηρες χωρις κενα."
                                                         "Δοκιμαστε παλι.")
                return

            if (not validate_input_only_letters(ap_lastname)):
                tk.messagebox.showerror("Λαθος Εισοδος", "Παρακαλω για το Επώνυμο χρησιμοποιήστε μόνο\n"
                                                         "Ελληνικους η Λατινικους χαρακτηρες χωρις κενα."
                                                         "Δοκιμαστε παλι.")
                return

            if ((not validate_input_only_numbers(ap_mobile)) or (not len(ap_mobile) == 10)):
                tk.messagebox.showerror("Λαθος Εισοδος", "Λαθος μορφη τηλεφωνου. "
                                                         "Επιτρεπονται μόνο 10αψηφιοι θετικοι αριθμοι."
                                                         "Δοκιμαστε παλι.")
                return

            if (not validate_input_email(ap_email)):
                tk.messagebox.showerror("Λαθος Εισοδος", "Λαθος μορφη email. "
                                                         "Επιτρεπονται μόνο πεζοι Λατινικοι χαρακτηρες, @ και . χωρις κενα."
                                                         "Δοκιμαστε παλι.")
                return

#περνάει τα στοιχεία στα περνάει functions και φτιάχνω τον πελάτη
            newcustomer = Customer.create(ap_firstname, ap_lastname, ap_mobile, ap_email)
            clear_content_frame(content_frame)
            label = ttk.Label(content_frame, text="Ο πελατης δημιουργηθηκε επιτυχώς.\n" + str(newcustomer))
            label.pack(fill=tk.X, padx=5, pady=5)

        def focus_next_window(event):
# περναει το focus στο επομενο widget
            event.widget.tk_focusNext().focus()
            return ("break")

# φτιάχνω τα widgets του παραθύρου 
        label = ttk.Label(content_frame, text="Όνομα:")
        label.pack(fill=tk.X, padx=5, pady=5)

        textbox_firstname = tk.Text(content_frame, height=1, width=10)
        textbox_firstname.bind("<Tab>", focus_next_window)
        textbox_firstname.pack(fill=tk.X, padx=5, pady=5)

        label = ttk.Label(content_frame, text="Επώνυμο:")
        label.pack(fill=tk.X, padx=5, pady=5)

        textbox_lastname = tk.Text(content_frame, height=1, width=10)
        textbox_lastname.bind("<Tab>", focus_next_window)
        textbox_lastname.pack(fill=tk.X, padx=5, pady=5)

        label = ttk.Label(content_frame, text="Τηλέφωνο:")
        label.pack(fill=tk.X, padx=5, pady=5)

        textbox_phone = tk.Text(content_frame, height=1, width=10)
        textbox_phone.bind("<Tab>", focus_next_window)
        textbox_phone.pack(fill=tk.X, padx=5, pady=5)

        label = ttk.Label(content_frame, text="Email:")
        label.pack(fill=tk.X, padx=5, pady=5)

        textbox_email = tk.Text(content_frame, height=1, width=10)
        textbox_email.bind("<Tab>", focus_next_window)
        textbox_email.pack(fill=tk.X, padx=5, pady=5)

        #βάζω τα κουτιά σε δικό τους frame και χρησιμοποιώ gride για να τα βάλω το ένα δίπλα στο άλλο
        btn_frame = tk.Frame(content_frame)
        btn_frame.configure(bg="#282830")
        btn_frame.pack(anchor=tk.N, expand=True, side=tk.LEFT)

        ok_btn = tk.Button(btn_frame, text="Δημιουργία", command=lambda: retrieve_input())
        ok_btn.grid(row=0, column=0, padx=10)
        cancel_btn = tk.Button(btn_frame, text="Ακύρωση", command=lambda: clear_content_frame(content_frame))
        cancel_btn.grid(row=0, column=1)

# funcion για την επεξεργασία πελάτη
    def modify_customer_clicked(event=None):
     
       #Βρίσκει και διαγράφει όλα τα widgets μέσα στο frame που καλούμε

        clear_content_frame(content_frame)
        #φέρνει όλους τους πελάτες, ή προβάλλει μύνημα σε περιπτωση όπου δεν υπάρχουν

        if (no_customers()):
            tk.messagebox.showerror("Προσοχη!", "Δεν υπάρχουν πελάτες στην βάση!\n"
                                                "Πηγαίνετε πρώτα στο μενού πελάτες\Δημιουργία "
                                                "για να δημιουργήσετε καινούργιους πελάτες.")
            return
        customers_list = Customer.get_table_rows()

        customerIDs = {}
        counter = 0
        for customer in customers_list:
            customerIDs[counter] = customer.id
            counter = counter + 1

# παίρνει τις αλλαγές από τα αντίστοιχα πεδία 

        def retrieve_input():
            customer_cb_selected_index = customer_cb.current()
            if (customer_cb_selected_index == -1):
                return

            ap_firstname = textbox_firstname.get("1.0", "end-1c")
            ap_lastname = textbox_lastname.get("1.0", "end-1c")
            ap_mobile = textbox_phone.get("1.0", "end-1c")
            ap_email = textbox_email.get("1.0", "end-1c")

            if (not validate_input_only_letters(ap_firstname)):
                tk.messagebox.showerror("Λαθος Εισοδος", "Παρακαλω για το όνομα χρησιμοποιήστε μόνο\n "
                                                         "Ελληνικους η Λατινικους χαρακτηρες χωρις κενα και τόνους."
                                                         "Δοκιμαστε παλι.")
                return

            if (not validate_input_only_letters(ap_lastname)):
                tk.messagebox.showerror("Λαθος Εισοδος", "Παρακαλω για το Επώνυμο χρησιμοποιήστε μόνο\n"
                                                         "Ελληνικους η Λατινικους χαρακτηρες χωρις κενα και τόνους."
                                                         "Δοκιμαστε παλι.")
                return

            if ((not validate_input_only_numbers(ap_mobile)) or (not len(ap_mobile) == 10)):
                tk.messagebox.showerror("Λαθος Εισοδος", "Λαθος μορφη τηλεφωνου. "
                                                         "Επιτρεπονται μόνο 10αψηφιοι θετικοι αριθμοι."
                                                         "Δοκιμαστε παλι.")
                return

            if (not validate_input_email(ap_email)):
                tk.messagebox.showerror("Λαθος Εισοδος", "Λαθος μορφη email. "
                                                         "Επιτρεπονται μόνο πεζοι Λατινικοι χαρακτηρες, @ και . χωρις κενα."
                                                         "Δοκιμαστε παλι.")
                return

#περνάει τα στοιχεία στα αντίστοιχα functions και καθαρίζει το παράθυρο
            tmpcustomer = customers_list[customer_cb_selected_index]
            tmpcustomer.change_firstname(ap_firstname)
            tmpcustomer.change_lastname(ap_lastname)
            tmpcustomer.change_mobile(ap_mobile)
            tmpcustomer.change_email(ap_email)
            clear_content_frame(content_frame)
            label = ttk.Label(content_frame, text="Ο πελατης ενημερωθηκε επιτυχώς.\n" + str(tmpcustomer))
            label.pack(fill=tk.X, padx=5, pady=5)

        def display_customer_info():
            #γεμίζει τα πεδία με τα στοιχεία του πελάτη
            customer_cb_selected_index = customer_cb.current()
            tmpcustomer = customers_list[customer_cb_selected_index]
            textbox_firstname.delete("1.0", "end-1c")
            textbox_firstname.insert("end-1c", tmpcustomer.firstname)
            textbox_lastname.delete("1.0", "end-1c")
            textbox_lastname.insert("end-1c", tmpcustomer.lastname)
            textbox_phone.delete("1.0", "end-1c")
            textbox_phone.insert("end-1c", tmpcustomer.mobile)
            textbox_email.delete("1.0", "end-1c")
            textbox_email.insert("end-1c", tmpcustomer.email)

        def focus_next_window(event):
            # περναει το focus στο επομενο widget
            event.widget.tk_focusNext().focus()
            return ("break")

        # Φτιάχνει και τοποθετεί τα widgets του παραθύρου
        label = ttk.Label(content_frame, text="Επιλέξτε πελάτη:")
        label.pack(fill=tk.X, padx=5, pady=5)

        selected_customer = tk.StringVar()

        # χρησιμοποιούμε Combobox για να αποτρέψουμε τον χρήστη να κάνει λάθοι
        customer_cb = ttk.Combobox(content_frame, textvariable=selected_customer)

        customer_cb['values'] = [customers_list[m] for m in range(len(customers_list))]

        
        customer_cb['state'] = 'readonly'

        
        customer_cb.pack(fill=tk.X, padx=5, pady=5)

        customer_cb.bind("<<ComboboxSelected>>", lambda _: display_customer_info())

       
        label = ttk.Label(content_frame, text="Όνομα:")
        label.pack(fill=tk.X, padx=5, pady=5)

        textbox_firstname = tk.Text(content_frame, height=1, width=10)
        textbox_firstname.bind("<Tab>", focus_next_window)
        textbox_firstname.pack(fill=tk.X, padx=5, pady=5)

        label = ttk.Label(content_frame, text="Επώνυμο:")
        label.pack(fill=tk.X, padx=5, pady=5)

        textbox_lastname = tk.Text(content_frame, height=1, width=10)
        textbox_lastname.bind("<Tab>", focus_next_window)
        textbox_lastname.pack(fill=tk.X, padx=5, pady=5)

        label = ttk.Label(content_frame, text="Τηλέφωνο:")
        label.pack(fill=tk.X, padx=5, pady=5)

        textbox_phone = tk.Text(content_frame, height=1, width=10)
        textbox_phone.bind("<Tab>", focus_next_window)
        textbox_phone.pack(fill=tk.X, padx=5, pady=5)

        label = ttk.Label(content_frame, text="Email:")
        label.pack(fill=tk.X, padx=5, pady=5)

        textbox_email = tk.Text(content_frame, height=1, width=10)
        textbox_email.bind("<Tab>", focus_next_window)
        textbox_email.pack(fill=tk.X, padx=5, pady=5)

        #βάζω τα κουτιά σε δικό τους frame και χρησιμοποιώ gride για να τα βάλω το ένα δίπλα στο άλλο
        btn_frame = tk.Frame(content_frame)
        btn_frame.configure(bg="#282830")
        btn_frame.pack(anchor=tk.N, expand=True, side=tk.LEFT)

        ok_btn = tk.Button(btn_frame, text="Ενημέρωση", command=lambda: retrieve_input())
        ok_btn.grid(row=0, column=0, padx=10)
        cancel_btn = tk.Button(btn_frame, text="Ακύρωση", command=lambda: clear_content_frame(content_frame))
        cancel_btn.grid(row=0, column=1)


    def delete_customer_clicked(event=None):

   #Function για την διαγραφή χρηστών

        #Βρίσκει και διαγράφει όλα τα widgets μέσα στο frame που καλούμε

        clear_content_frame(content_frame)

        #φέρνει όλους τους πελάτες, ή προβάλλει μύνημα σε περιπτωση όπου δεν υπάρχουν

        if (no_customers()):
            tk.messagebox.showerror("Προσοχη!", "Δεν υπάρχουν πελάτες στην βάση!\n"
                                                "Πηγαίνετε πρώτα στο μενού πελάτες\Δημιουργία "
                                                "για να δημιουργήσετε καινούργιους πελάτες.")
            return
        customers_list = Customer.get_table_rows()

        def retrieve_input():
            customer_cb_selected_index = customer_cb.current()
            if (customer_cb_selected_index == -1):
                return

            if (not tk.messagebox.askokcancel("Προσοχη!", "Προσοχη! \nΕχετε επιλεξει να διαγραψετε τον πελάτη\n\n"
                                                          + str(customers_list[customer_cb_selected_index]) +
                                                          "\n\nΘα διαγραφουν μαζι και ολα του τα ραντεβού."
                                                          "\nΕιστε σιγουροι;")):
                return

            customerIDs = {}
            counter = 0
            for customer in customers_list:
                customerIDs[counter] = customer.id
                counter = counter + 1


    
            if (not no_appointments()):
                delete_appointments_of_customerid(customerIDs[customer_cb_selected_index])
            tmpcustomer = customers_list[customer_cb_selected_index]
            tmpcustomer.delete()

            clear_content_frame(content_frame)
            label = ttk.Label(content_frame,
                              text="Ο πελατης διαγράφηκε επιτυχώς.\n" + str(customers_list[customer_cb_selected_index]))
            label.pack(fill=tk.X, padx=5, pady=5)

            #Διαγράφει τους πελάτες και τα ραντεβού τους

        # Φτιάχνει και τοποθετεί τα widgets του παραθύρου
        label = ttk.Label(content_frame, text="Επιλέξτε πελάτη:")
        label.pack(fill=tk.X, padx=5, pady=5)

# χρησιμοποιούμε Combobox για να αποτρέψουμε τον χρήστη να κάνει λάθοι

        selected_customer = tk.StringVar()
        customer_cb = ttk.Combobox(content_frame, textvariable=selected_customer)

        customer_cb['values'] = [customers_list[m] for m in range(len(customers_list))]

        customer_cb['state'] = 'readonly'

        customer_cb.pack(fill=tk.X, padx=5, pady=5)

        #βάζω τα κουτιά σε δικό τους frame και χρησιμοποιώ gride για να τα βάλω το ένα δίπλα στο άλλο
        btn_frame = tk.Frame(content_frame)
        btn_frame.configure(bg="#282830")
        btn_frame.pack(anchor=tk.N, expand=True, side=tk.LEFT)

        ok_btn = tk.Button(btn_frame, text="Διαγραφή", command=lambda: retrieve_input())
        ok_btn.grid(row=0, column=0, padx=10)
        cancel_btn = tk.Button(btn_frame, text="Ακύρωση", command=lambda: clear_content_frame(content_frame))
        cancel_btn.grid(row=0, column=1)


    def new_appointment_clicked(event=None):
        # funcion για την δημιουργία πελάτη
        
        #Βρίσκει και διαγράφει όλα τα widgets μέσα στο frame που καλούμε

        clear_content_frame(content_frame)

        #φέρνει όλους τους πελάτες, ή προβάλλει μύνημα σε περιπτωση όπου δεν υπάρχουν
        if (no_customers()):
            tk.messagebox.showerror("Προσοχη!", "Δεν υπάρχουν πελάτες στην βάση!\n"
                                                "Πηγαίνετε πρώτα στο μενού πελάτες\Δημιουργία "
                                                "για να δημιουργήσετε καινούργιους πελάτες.")
            return
        customers_list = Customer.get_table_rows()



#περνάει τα στοιχεία στα functions και φτιάχνει το ραντεβού 
        def retrieve_input():
            customer_cb_selected_index = customer_cb.current()
            if (customer_cb_selected_index == -1):
                return

            customerIDs = {}
            counter = 0
            for customer in customers_list:
                customerIDs[counter] = customer.id
                counter = counter + 1

            ap_customerid = customerIDs[customer_cb_selected_index]
            ap_datetime = str(cal.get()) + ' ' + str(hour_cb.get()) + ':' + str(minutes_cb.get())
            ap_duration = duration_cb.get()

            if (not no_overlapping_appointments(ap_datetime, ap_duration)):
                tk.messagebox.showerror("Λαθος Εισοδος", "Ο συνδιασμος ημερομηνιας/ωρας και διαρκειας "
                                                         "\nπου βαλατε ειναι ηδη δεσμευμενος απο αλλο ραντεβού."
                                                         "\nΔοκιμαστε παλι.")
                return

            newappointment = Appointment.create(ap_customerid, ap_datetime, ap_duration)
            clear_content_frame(content_frame)
            label = ttk.Label(content_frame, text="Το ραντεβού δημιουργηθηκε επιτυχώς.\n" + str(newappointment))
            label.pack(fill=tk.X, padx=5, pady=5)

        # φτιάχνω τα widgets του παραθύρου 

        # χρησιμοποιούμε Combobox για να αποτρέψουμε τον χρήστη να κάνει λάθοι

        label = ttk.Label(content_frame, text="Επιλέξτε πελάτη:")
        label.pack(fill=tk.X, padx=5, pady=5)
       
        selected_customer = tk.StringVar()
        customer_cb = ttk.Combobox(content_frame, textvariable=selected_customer)

        customer_cb['values'] = [customers_list[m] for m in range(len(customers_list))]

        customer_cb['state'] = 'readonly'

        customer_cb.pack(fill=tk.X, padx=5, pady=5)

    
        label = ttk.Label(content_frame, text="Επιλέξτε Ημερομηνία:")
        label.pack(fill=tk.X, padx=5, pady=5)

        cal = DateEntry(content_frame, locale='en_US', date_pattern='YYYY-mm-dd',
                        width=12, year=datetime.now().year, month=datetime.now().month, day=datetime.now().day,
                        borderwidth=2)

        cal.pack(fill=tk.X, padx=5, pady=5)

        label = ttk.Label(content_frame, text="Επιλέξτε Ώρα:")
        label.pack(fill=tk.X, padx=5, pady=5)

        hour_cb = ttk.Combobox(content_frame)
        hours_list = [*range(0, 24)]
        hour_cb['values'] = [str(element).rjust(2, '0') for element in hours_list]

        hour_cb.current(datetime.now().hour)
        hour_cb['state'] = 'readonly'
        hour_cb.pack(fill=tk.X, padx=5, pady=5)

        minutes_cb = ttk.Combobox(content_frame)
        minites_int_list = [*range(0, 60)]
        minutes_cb['values'] = [str(element).rjust(2, '0') for element in minites_int_list]

        minutes_cb.current(datetime.now().minute)

        minutes_cb['state'] = 'readonly'

        minutes_cb.pack(fill=tk.X, padx=5, pady=5)

        label = ttk.Label(content_frame, text="Επιλέξτε Διάρκεια:")
        label.pack(fill=tk.X, padx=5, pady=5)

        selected_duration = tk.StringVar()
        duration_cb = ttk.Combobox(content_frame)

        duration_cb['values'] = [5, 10, 15, 30, 60, 90, 120]

        duration_cb.current(3)

        duration_cb['state'] = 'readonly'

        duration_cb.pack(fill=tk.X, padx=5, pady=5)

        #βάζω τα κουτιά σε δικό τους frame και χρησιμοποιώ gride για να τα βάλω το ένα δίπλα στο άλλο
        btn_frame = tk.Frame(content_frame)
        btn_frame.configure(bg="#282830")
        btn_frame.pack(anchor=tk.N, expand=True, side=tk.LEFT)

        ok_btn = tk.Button(btn_frame, text="Δημιουργία", command=lambda: retrieve_input())
        ok_btn.grid(row=0, column=0, padx=10)
        cancel_btn = tk.Button(btn_frame, text="Ακύρωση", command=lambda: clear_content_frame(content_frame))
        cancel_btn.grid(row=0, column=1)


    def modify_appointment_clicked(event=None):
        # funcion για την επεξεργασία ραντεβού

        #Βρίσκει και διαγράφει όλα τα widgets μέσα στο frame που καλούμε
        clear_content_frame(content_frame)

        customers_list = Customer.get_table_rows()

        #φέρνει όλα τα ραντεβού, ή προβάλλει μύνημα σε περιπτωση όπου δεν υπάρχουν
        
        if (no_appointments()):
            tk.messagebox.showerror("Προσοχη!", "Δεν υπάρχουν ραντεβού στην βάση!\n"
                                                "Πηγαίνετε πρώτα στο μενού ραντεβού\Δημιουργία "
                                                "για να δημιουργήσετε καινούργια ραντεβού.")
            return
        appointments_tablerows = list_appointments_with_customer_fullname()
        appointments_list = Appointment.get_table_rows()

#περνάει τα στοιχεία στα functions και επεξεργάζεται το ραντεβού 

        def retrieve_input():
            appointment_cb_selected_index = appointment_cb.current()
            if (appointment_cb_selected_index == -1):
                return

            customerIDs = {}
            counter = 0
            for customer in customers_list:
                customerIDs[counter] = customer.id
                counter = counter + 1

            appointmentIDs = {}
            counter = 0
            for appointment in appointments_list:
                appointmentIDs[counter] = appointment.id
                counter = counter + 1

            ap_customerid = customerIDs[customer_cb.current()]
            ap_datetime = str(cal.get()) + ' ' + str(hour_cb.get()) + ':' + str(minutes_cb.get())
            ap_duration = duration_cb.get()

            # Τυπώνει μήνυμα σε περίπτωση που οι ώρες είναι δεσμευμένες
            if (not no_overlapping_appointments(ap_datetime, ap_duration)):
                tk.messagebox.showerror("Λαθος Εισοδος", "Ο συνδιασμος ημερομηνιας/ωρας και διαρκειας "
                                                         "\nπου βαλατε ειναι ηδη δεσμευμενος απο αλλο ραντεβού."
                                                         "\nΔοκιμαστε παλι.")
                return

            tmpappointment = appointments_list[appointment_cb_selected_index]
            tmpappointment.change_customerid(ap_customerid)
            tmpappointment.change_datetime(ap_datetime)
            tmpappointment.change_duration(ap_duration)

            clear_content_frame(content_frame)
            label = ttk.Label(content_frame, text="Το ραντεβού ενημερωθηκε επιτυχώς.\n" + str(tmpappointment))
            label.pack(fill=tk.X, padx=5, pady=5)

        #γεμίζει τα πεδία με τα στοιχεία του πελάτη

        def display_appointment_info():
            appointment_cb_selected_index = appointment_cb.current()
            tmpappointment = appointments_list[appointment_cb_selected_index]

            customerIDs = {}
            counter = 0
            for customer in customers_list:
                customerIDs[customer.id] = counter
                counter = counter + 1

            ap_customerid = customerIDs[tmpappointment.customerid]

            customer_cb.current(ap_customerid)

            datetime_obj = datetime.strptime(tmpappointment.datetime,
                                             "%Y-%m-%d %H:%M")

            hoursIndex = {}
            counter = 0
            for value in hour_cb['values']:
                hoursIndex[int(value)] = counter
                counter = counter + 1
            hour_cb.current(hoursIndex[datetime_obj.hour])

            minutesIndex = {}
            counter = 0
            for value in minutes_cb['values']:
                minutesIndex[int(value)] = counter
                counter = counter + 1

            minutes_cb.current(minutesIndex[datetime_obj.minute])

            cal.set_date(datetime_obj.date())

            durationIndex = {}
            counter = 0
            for value in duration_cb['values']:
                durationIndex[int(value)] = counter
                counter = counter + 1

            duration_cb.current(durationIndex[tmpappointment.duration])

            def focus_next_window(event):
                # περναει το focus στο επομενο widget
                event.widget.tk_focusNext().focus()
                return ("break")

       # Φτιάχνει και τοποθετεί τα widgets του παραθύρου

        label = ttk.Label(content_frame, text="Επιλέξτε ρεντεβού:")
        label.pack(fill=tk.X, padx=5, pady=5)

# χρησιμοποιούμε Combobox για να αποτρέψουμε τον χρήστη να κάνει λάθοι

        selected_appointment = tk.StringVar()
        appointment_cb = ttk.Combobox(content_frame)

        appointment_cb['values'] = [appointments_tablerows[m] for m in range(len(appointments_tablerows))]

        appointment_cb['state'] = 'readonly'

        appointment_cb.pack(fill=tk.X, padx=5, pady=5)

        label = ttk.Label(content_frame, text="Επιλέξτε πελάτη:")
        label.pack(fill=tk.X, padx=5, pady=5)

        selected_customer = tk.StringVar()
        customer_cb = ttk.Combobox(content_frame)

        customer_cb['values'] = [customers_list[m] for m in range(len(customers_list))]

        customer_cb['state'] = 'readonly'

        customer_cb.pack(fill=tk.X, padx=5, pady=5)

        label = ttk.Label(content_frame, text="Επιλέξτε Ημερομηνία:")
        label.pack(fill=tk.X, padx=5, pady=5)

        cal = DateEntry(content_frame, locale='en_US', date_pattern='YYYY-mm-dd',
                        width=12, year=datetime.now().year, month=datetime.now().month, day=datetime.now().day,
                        borderwidth=2)

        cal.pack(fill=tk.X, padx=5, pady=5)

        label = ttk.Label(content_frame, text="Επιλέξτε Ώρα:")
        label.pack(fill=tk.X, padx=5, pady=5)

        hour_cb = ttk.Combobox(content_frame)
        hours_list = [*range(0, 24)]
        hour_cb['values'] = [str(element).rjust(2, '0') for element in hours_list]

        hour_cb.current(datetime.now().hour)

        hour_cb['state'] = 'readonly'

        hour_cb.pack(fill=tk.X, padx=5, pady=5)

        minutes_cb = ttk.Combobox(content_frame)
        minites_int_list = [*range(0, 60)]
        minutes_cb['values'] = [str(element).rjust(2, '0') for element in minites_int_list]
        minutes_cb.current(datetime.now().minute)

        minutes_cb['state'] = 'readonly'

        minutes_cb.pack(fill=tk.X, padx=5, pady=5)

        label = ttk.Label(content_frame, text="Επιλέξτε Διάρκεια:")
        label.pack(fill=tk.X, padx=5, pady=5)

        selected_duration = tk.StringVar()
        duration_cb = ttk.Combobox(content_frame)

        duration_cb['values'] = [5, 10, 15, 30, 60, 90, 120]

        duration_cb.current(3)

        duration_cb['state'] = 'readonly'

        duration_cb.pack(fill=tk.X, padx=5, pady=5)

        appointment_cb.bind("<<ComboboxSelected>>", lambda _: display_appointment_info())

        #βάζω τα κουτιά σε δικό τους frame και χρησιμοποιώ gride για να τα βάλω το ένα δίπλα στο άλλο
        btn_frame = tk.Frame(content_frame)
        btn_frame.configure(bg="#282830")
        btn_frame.pack(anchor=tk.N, expand=True, side=tk.LEFT)

        ok_btn = tk.Button(btn_frame, text="Ενημέρωση", command=lambda: retrieve_input())
        ok_btn.grid(row=0, column=0, padx=10)
        cancel_btn = tk.Button(btn_frame, text="Ακύρωση", command=lambda: clear_content_frame(content_frame))
        cancel_btn.grid(row=0, column=1)


    def delete_appointment_clicked(event=None):
        #Βρίσκει και διαγράφει όλα τα widgets μέσα στο frame που καλούμε
        clear_content_frame(content_frame)

        #φέρνει όλα τα ραντεβού, ή προβάλλει μύνημα σε περιπτωση όπου δεν υπάρχουν
      
        if (no_appointments()):
            tk.messagebox.showerror("Προσοχη!", "Δεν υπάρχουν ραντεβού στην βάση!\n"
                                                "Πηγαίνετε πρώτα στο μενού ραντεβού\Δημιουργία "
                                                "για να δημιουργήσετε καινούργια ραντεβού.")
            return
        appointments_tablerows = list_appointments_with_customer_fullname()
        appointments_list = Appointment.get_table_rows()
        appointmentIDs = {}

#περνάει τα στοιχεία στα functions και διαγράφει το ραντεβού 

        def retrieve_input():
            appointment_cb_selected_index = appointment_cb.current()
            if (appointment_cb_selected_index == -1):
                return

            if (not tk.messagebox.askokcancel("Προσοχη!", "Προσοχη! \nΕχετε επιλεξει να διαγραψετε το ραντεβού\n\n"
                                                          + str(appointments_list[appointment_cb_selected_index]) +
                                                          "\n\nΕιστε σιγουροι;")):
                return

            counter = 0
            for appointment in appointments_list:
                appointmentIDs[counter] = appointment.id
                counter = counter + 1

            tmpappointment = appointments_list[appointment_cb_selected_index]
            tmpappointment.delete()

            clear_content_frame(content_frame)
            label = ttk.Label(content_frame, text="Το ραντεβού διαγράφηκε επιτυχώς.\n" + str(
                appointments_list[appointment_cb_selected_index]))
            label.pack(fill=tk.X, padx=5, pady=5)

# φτιάχνω τα widgets του παραθύρου 

        label = ttk.Label(content_frame, text="Επιλέξτε ρεντεβού:")
        label.pack(fill=tk.X, padx=5, pady=5)

        # χρησιμοποιούμε Combobox για να αποτρέψουμε τον χρήστη να κάνει λάθοι
        selected_appointment = tk.StringVar()
        appointment_cb = ttk.Combobox(content_frame, textvariable=selected_appointment)

        appointment_cb['values'] = [appointments_tablerows[m] for m in range(len(appointments_tablerows))]

        appointment_cb['state'] = 'readonly'

        appointment_cb.pack(fill=tk.X, padx=5, pady=5)

        #βάζω τα κουτιά σε δικό τους frame και χρησιμοποιώ gride για να τα βάλω το ένα δίπλα στο άλλο
        btn_frame = tk.Frame(content_frame)
        btn_frame.configure(bg="#282830")
        btn_frame.pack(anchor=tk.N, expand=True, side=tk.LEFT)

        ok_btn = tk.Button(btn_frame, text="Διαγραφή", command=lambda: retrieve_input())
        ok_btn.grid(row=0, column=0, padx=10)
        cancel_btn = tk.Button(btn_frame, text="Ακύρωση", command=lambda: clear_content_frame(content_frame))
        cancel_btn.grid(row=0, column=1)


    def search_by_date_gui():
        #Function για να ψάξει μέσω ημερομηνιών
        #Βρίσκει και διαγράφει όλα τα widgets μέσα στο frame που καλούμε
        clear_content_frame(content_frame)
       
        #φέρνει όλα τα ραντεβού, ή προβάλλει μύνημα σε περιπτωση όπου δεν υπάρχουν

        if (no_appointments()):
            tk.messagebox.showerror("Προσοχη!", "Δεν υπάρχουν ραντεβού στην βάση!\n"
                                                "Πηγαίνετε πρώτα στο μενού ραντεβού\Δημιουργία "
                                                "για να δημιουργήσετε καινούργια ραντεβού.")
            return


        def search_and_show_results():
        #Αναζητάει την ημερομινία και σε περίπτωση που υπάρχουν καλή την show_results_window
            date = cal.get_date()
            if date:
                results = search_by_date(date)
                if results:
                    show_results_window(results)
                else:
                    messagebox.showinfo("No Results", "No results found.")

        # φτιάχνω τα widgets του παραθύρου 

        label_date = tk.Label(content_frame, text="Παρακαλω επιλέξτε Ημερομηνία:")
        label_date.pack(padx=5, pady=5)
        cal = DateEntry(content_frame, width=12, background='darkblue', foreground='white', borderwidth=2,
                        date_pattern='yyyy-mm-dd')
        cal.pack(fill=tk.X, padx=5, pady=5)

        button_search = tk.Button(content_frame, text="Αναζήτηση", command=search_and_show_results)
        button_search.pack(pady=5)


    # button_return = tk.Button(content_frame, text="Επιστροφή στο Μενού Αναζήτησης", command=lambda: return_to_main_menu(main_menu, content_frame))
    # button_return.pack(pady=5)

    def search_by_email_gui():
        #Βρίσκει και διαγράφει όλα τα widgets μέσα στο frame που καλούμε
        clear_content_frame(content_frame)
    
        #φέρνει όλα τα ραντεβού, ή προβάλλει μύνημα σε περιπτωση όπου δεν υπάρχουν
      
        if (no_appointments()):
            tk.messagebox.showerror("Προσοχη!", "Δεν υπάρχουν ραντεβού στην βάση!\n"
                                                "Πηγαίνετε πρώτα στο μενού ραντεβού\Δημιουργία "
                                                "για να δημιουργήσετε καινούργια ραντεβού.")
            return

        def search_and_show_results():
            #Αναζητάει τo email και σε περίπτωση που υπάρχουν καλή την show_results_window
            email = entry_email.get()
            if email:
                results = search_by_customer_email(email)
                if results:
                    show_results_window(results)
                else:
                    messagebox.showinfo("No Results", "Δεν βρέθηκαν αποτελέσματα.")

        # φτιάχνω τα widgets του παραθύρου 

        label_email = tk.Label(content_frame, text="Παρακαλώ εισάγετε το email του πελάτη:")
        label_email.pack(padx=5, pady=5)
        entry_email = tk.Entry(content_frame)
        entry_email.pack(fill=tk.X, padx=5, pady=5)

        button_search = tk.Button(content_frame, text="Αναζήτηση", command=search_and_show_results)
        button_search.pack(pady=5)


    def show_results_window(results):
        #Έμφανίζει τα αποτελέσματα από το search 
        #Βρίσκει και διαγράφει όλα τα widgets μέσα στο frame που καλούμε
        clear_content_frame(content_frame)

        def export_to_excel_window():
            #Καλώ function που δημιουργεί excel με τα αποτελέσματα από το search 

            nonlocal button_export_excel
            button_export_excel.destroy()

            def export():

                filename = entry_filename.get()
                if filename:
                    try:
                        export_to_excel(results, filename + ".xlsx")
                        clear_content_frame(content_frame)
                        tk.messagebox.showinfo("Πληροφορία", f"Εξαγωγή σε Excel με όνομα {filename}.xlsx")
                    except:
                        tk.messagebox.showerror("Προσοχή!", "Παρσουσιάστηκε πρόβλημα κατά την δημιουργεία του αρχείου.")

            # φτιάχνω τα widgets του παραθύρου 

            label_filename = tk.Label(content_frame, text="Πληκτολογείστε το όνομα αρχείου Excel (χωρις κατάληξη):")
            label_filename.pack()

            entry_filename = tk.Entry(content_frame)
            entry_filename.pack()

            #βάζω τα κουτιά σε δικό τους frame και χρησιμοποιώ gride για να τα βάλω το ένα δίπλα στο άλλο
            btn_frame = tk.Frame(content_frame)
            btn_frame.configure(bg="#282830")
            btn_frame.pack(anchor=tk.N, expand=True, side=tk.LEFT)

            cancel_btn = tk.Button(btn_frame, text="Ακύρωση", command=lambda: clear_content_frame(content_frame))
            cancel_btn.grid(row=0, column=1, padx=10)
            button_export = tk.Button(btn_frame, text="Εξαγωγή", command=export)
            button_export.grid(row=0, column=0)

        headers = ("Κωδικός", "Όνομα", "Επίθετο", "Ημερομηνία/Ώρα Ραντεβού", "Διάρκεια", "Email")

        frame = customtkinter.CTkScrollableFrame(content_frame)
        frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        frame.config(width=815)

        # Προσθήκη κεφαλίδων
        for col, header in enumerate(headers):
            label_header = tk.Label(frame, text=header, font=("Helvetica", 10, "bold"), padx=10, pady=5,
                                    relief=tk.RIDGE)
            label_header.grid(row=0, column=col, sticky="nsew")

        # Εμφάνιση δεδομένων
        for row, result in enumerate(results, start=1):
            # Εμφάνιση ID
            label_id = tk.Label(frame, text=result[0], padx=10, pady=5, relief=tk.RIDGE)
            label_id.grid(row=row, column=0, sticky="nsew")

            # Εμφάνιση υπολοίπων δεδομένων
            for col, data in enumerate(result[1:], start=1):
                label_data = tk.Label(frame, text=data, padx=10, pady=5, relief=tk.RIDGE)
                label_data.grid(row=row, column=col, sticky="nsew")

        button_export_excel = tk.Button(content_frame, text="Εξαγωγή σε Excel", command=export_to_excel_window)
        button_export_excel.pack()


    def reminder():
        #Βρίσκει και διαγράφει όλα τα widgets μέσα στο frame που καλούμε
        clear_content_frame(content_frame)

        #φέρνει όλα τα ραντεβού, ή προβάλλει μύνημα σε περιπτωση όπου δεν υπάρχουν
   
        if (no_appointments()):
            tk.messagebox.showerror("Προσοχη!", "Δεν υπάρχουν ραντεβού στην βάση!\n"
                                                "Πηγαίνετε πρώτα στο μενού ραντεβού\Δημιουργία "
                                                "για να δημιουργήσετε καινούργια ραντεβού.")
            return
        
       # φτιάχνω τα widgets του παραθύρου 

        label_email = tk.Label(content_frame, text="Παρακαλώ εισάγετε το email του πελάτη:")
        label_email.pack(padx=5, pady=5)
        label = ttk.Label(content_frame, text="Επιλέξτε Ημερομηνία:")
        label.pack(fill=tk.X, padx=5, pady=5)


        entry = DateEntry(content_frame, locale='en_US', date_pattern='YYYY-mm-dd',
                          width=12, year=datetime.now().year, month=datetime.now().month, day=datetime.now().day,
                          borderwidth=2)

        entry.pack(fill=tk.X, padx=5, pady=5)

        def search_and_display_results():


            date = entry.get()
            results = search_by_date(date)

            #Εμφανίζω τα ραντεβού που αντιστοιχούν στην ημερομηνία ή τυπώνω μήνυμα σε περίπτωση που δεν υπάρχει 

            if results:
                clear_content_frame(content_frame)
                ResultFrame = tk.Frame(content_frame, bg="#282830")
                ResultFrame.pack(anchor=tk.N, fill=tk.BOTH, expand=True, side=tk.BOTTOM)
                for result in results:
                    customer_name = f"{result[1]} {result[2]}"
                    appointment_datetime = result[3]

                    result_label = tk.Label(ResultFrame,
                                            text=f"Πελάτης: {customer_name}, Ημερομηνία: {appointment_datetime}")
                    result_label.pack(pady=5)

                send_button = tk.Button(ResultFrame, text="Αποστολή Email Υπενθύμισης",
                                        command=lambda: send_reminder(results))
                send_button.pack(pady=5)
            else:
                messagebox.showinfo("Καμία εγγραφή", "Δεν βρέθηκαν ραντεβού για την επιλεγμένη ημερομηνία.")

        #βάζω τα κουτιά σε δικό τους frame και χρησιμοποιώ gride για να τα βάλω το ένα δίπλα στο άλλο
        btn_frame = tk.Frame(content_frame)
        btn_frame.configure(bg="#282830")
        btn_frame.pack(anchor=tk.N, expand=True, side=tk.LEFT)

        button_search = tk.Button(btn_frame, text="Αναζήτηση", command=search_and_display_results)
        button_search.grid(row=0, column=0, padx=10)
        cancel_btn = tk.Button(btn_frame, text="Ακύρωση", command=lambda: clear_content_frame(content_frame))
        cancel_btn.grid(row=0, column=1)


# Φτιάχνω το Παράθυρο και του δίνω όνομα, icon, μέγεθος
    root = tk.Tk()
    root.title("Διαχείρηση ραντεβού - Project07")
    root.geometry("915x650")
    menubar = tk.Menu()

    #Φτιάχνω το menu και περνάω τις σελίδες  

    tk_search_by_date = tk.Menu(menubar, tearoff=False)
    tk_search_by_date.add_command(
        label="Με Ημερομηνία",
        command=search_by_date_gui,
        compound=tk.LEFT
    )
    tk_search_by_date.add_command(
        label="Με email",
        command=search_by_email_gui,
        compound=tk.LEFT
    )

    tk_customers_menu = tk.Menu(menubar, tearoff=False)
    tk_customers_menu.add_command(
        label="Δημιουργία",
        command=new_customer_clicked,
        compound=tk.LEFT
    )
    tk_customers_menu.add_command(
        label="Τροποποίηση",
        command=modify_customer_clicked,
        compound=tk.LEFT
    )
    tk_customers_menu.add_command(
        label="Διαγραφή",
        command=delete_customer_clicked,
        compound=tk.LEFT
    )

    tk_appointments_menu = tk.Menu(menubar, tearoff=False)
    tk_appointments_menu.add_command(
        label="Δημιουργία",
        command=new_appointment_clicked,
        compound=tk.LEFT
    )
    tk_appointments_menu.add_command(
        label="Τροποποίηση",
        command=modify_appointment_clicked,
        compound=tk.LEFT
    )
    tk_appointments_menu.add_command(
        label="Διαγραφή",
        command=delete_appointment_clicked,
        compound=tk.LEFT
    )

    tk_appointments_menu.add_separator()

    tk_appointments_menu.add_cascade(
        menu=tk_search_by_date,
        label="Αναζήτηση"
    )

    tk_appointments_menu.add_command(
        label="Υπενθύμιση",
        command=reminder,
        compound=tk.LEFT
    )

    tk_settings_menu = tk.Menu(menubar, tearoff=False)

    menubar.add_cascade(menu=tk_customers_menu, label="Πελάτες")
    menubar.add_cascade(menu=tk_appointments_menu, label="Ραντεβού")

    root.config(menu=menubar, bg="#282830")

    icon = tk.PhotoImage(file="assets/WindowLogo.png")
    root.iconphoto(True, icon)
    root.title("Διαχείρηση Ραντεβού")

    content_frame = tk.Frame(root, bg="#282830") 
    content_frame.pack(anchor=tk.N, fill=tk.BOTH, expand=True, side=tk.LEFT)

    logo_photo = load_logo(scale_factor=0.5)  # Φορτώνουμε το λογότυπο
    if logo_photo:
        label_logo = tk.Label(root, image=logo_photo, bg="#282830")
        label_logo.pack(side=tk.BOTTOM)

    root.mainloop()
