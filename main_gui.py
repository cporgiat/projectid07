import appointments_menu
import customers_menu
import search_menu
import print_menu
from tkcalendar import DateEntry
from search import search_by_date, search_by_customer_email, print_results, export_to_excel 
from tkinter import messagebox
from utils import get_number
from reminder import send_appointment_reminder
  
if __name__ == '__main__':
    import customtkinter
    import tkinter as tk
    from tkinter import ttk
    from tkinter import messagebox
    from datetime import datetime

    def load_logo(scale_factor=0.5):
     try:
        logo = tk.PhotoImage(file="Logo.png")
        logo = logo.subsample(int(1.5/scale_factor))  # Κλιμάκωση του λογότυπου
        return logo
     except tk.TclError as e:
        messagebox.showerror("Error", f"Failed to load logo: {e}")
        return None

    def clear_content_frame(frame):
        for widget in frame.winfo_children():
            widget.destroy()


    def new_customer_clicked(event=None):
        clear_content_frame(content_frame)

        def retrieve_input():
            from customers import Customer
            from utils import validate_input_email, validate_input_only_letters, validate_input_only_numbers
            ap_firstname = textbox_firstname.get("1.0", "end-1c")
            ap_lastname = textbox_lastname.get("1.0", "end-1c")
            ap_mobile = textbox_phone.get("1.0", "end-1c")
            ap_email = textbox_email.get("1.0", "end-1c")

            if(not validate_input_only_letters(ap_firstname)):
                tk.messagebox.showerror("Λαθος Εισοδος", "Παρακαλω για το Ονομα χρησιμοποιηστε μονο\n "
                                                "Ελληνικους η Λατινικους χαρακτηρες χωρις κενα."
                                                "Δοκιμαστε παλι.")
                return

            if(not validate_input_only_letters(ap_lastname)):
                tk.messagebox.showerror("Λαθος Εισοδος", "Παρακαλω για το Επωνυμο χρησιμοποιηστε μονο\n"
                                                "Ελληνικους η Λατινικους χαρακτηρες χωρις κενα."
                                                "Δοκιμαστε παλι.")
                return

            if((not validate_input_only_numbers(ap_mobile)) or (not len(ap_mobile)==9)):
                tk.messagebox.showerror("Λαθος Εισοδος", "Λαθος μορφη τηλεφωνου. "
                                                "Επιτρεπονται μονο 9αψηφιοι θετικοι αριθμοι."
                                                "Δοκιμαστε παλι.")
                return

            if(not validate_input_email(ap_email)):
                tk.messagebox.showerror("Λαθος Εισοδος", "Λαθος μορφη email. "
                                                "Επιτρεπονται μονο πεζοι Λατινικοι χαρακτηρες, @ και . χωρις κενα."
                                                "Δοκιμαστε παλι.")
                return

            newcustomer = Customer.create(ap_firstname, ap_lastname, ap_mobile, ap_email)
            clear_content_frame(content_frame)
            label = ttk.Label(content_frame, text="Ο πελατης δημιουργηθηκε επιτυχως.\n" + str(newcustomer))
            label.pack(fill=tk.X, padx=5, pady=5)

        # label
        label = ttk.Label(content_frame, text="Ονομα:")
        label.pack(fill=tk.X, padx=5, pady=5)

        textbox_firstname = tk.Text(content_frame, height=1, width=10)
        textbox_firstname.pack(fill=tk.X, padx=5, pady=5)

        label = ttk.Label(content_frame, text="Επωνυμο:")
        label.pack(fill=tk.X, padx=5, pady=5)

        textbox_lastname = tk.Text(content_frame, height=1, width=10)
        textbox_lastname.pack(fill=tk.X, padx=5, pady=5)

        label = ttk.Label(content_frame, text="Τηλεφωνο:")
        label.pack(fill=tk.X, padx=5, pady=5)

        textbox_phone = tk.Text(content_frame, height=1, width=10)
        textbox_phone.pack(fill=tk.X, padx=5, pady=5)

        label = ttk.Label(content_frame, text="Email:")
        label.pack(fill=tk.X, padx=5, pady=5)

        textbox_email = tk.Text(content_frame, height=1, width=10)
        textbox_email.pack(fill=tk.X, padx=5, pady=5)
        
        btn_frame = tk.Frame(content_frame)
        btn_frame.configure(bg= "#282830")
        btn_frame.pack(anchor=tk.N, expand=True, side=tk.LEFT)

        ok_btn = tk.Button(btn_frame, text="Δημιουργια", command=lambda: retrieve_input())
        ok_btn.grid(row=0,column=0,padx=10)
        cancel_btn = tk.Button(btn_frame, text="Ακυρωση", command=lambda: clear_content_frame(content_frame))
        cancel_btn.grid(row=0,column=1)


    def modify_customer_clicked(event=None):
        clear_content_frame(content_frame)

        from customers import Customer
        customers_list = Customer.get_table_rows()

        customerIDs = {}
        counter = 0
        for customer in customers_list:
            customerIDs[counter] = customer.id
            counter = counter + 1

        def retrieve_input():
            from utils import validate_input_email, validate_input_only_letters, validate_input_only_numbers
            customer_cb_selected_index = customer_cb.current()
            if(customer_cb_selected_index == -1):
                return

            ap_firstname = textbox_firstname.get("1.0", "end-1c")
            ap_lastname = textbox_lastname.get("1.0", "end-1c")
            ap_mobile = textbox_phone.get("1.0", "end-1c")
            ap_email = textbox_email.get("1.0", "end-1c")

            if(not validate_input_only_letters(ap_firstname)):
                tk.messagebox.showerror("Λαθος Εισοδος", "Παρακαλω για το Ονομα χρησιμοποιηστε μονο\n "
                                                "Ελληνικους η Λατινικους χαρακτηρες χωρις κενα."
                                                "Δοκιμαστε παλι.")
                return

            if(not validate_input_only_letters(ap_lastname)):
                tk.messagebox.showerror("Λαθος Εισοδος", "Παρακαλω για το Επωνυμο χρησιμοποιηστε μονο\n"
                                                "Ελληνικους η Λατινικους χαρακτηρες χωρις κενα."
                                                "Δοκιμαστε παλι.")
                return

            if((not validate_input_only_numbers(ap_mobile)) or (not len(ap_mobile)==9)):
                tk.messagebox.showerror("Λαθος Εισοδος", "Λαθος μορφη τηλεφωνου. "
                                                "Επιτρεπονται μονο 9αψηφιοι θετικοι αριθμοι."
                                                "Δοκιμαστε παλι.")
                return

            if(not validate_input_email(ap_email)):
                tk.messagebox.showerror("Λαθος Εισοδος", "Λαθος μορφη email. "
                                                "Επιτρεπονται μονο πεζοι Λατινικοι χαρακτηρες, @ και . χωρις κενα."
                                                "Δοκιμαστε παλι.")
                return

            tmpcustomer = customers_list[customer_cb_selected_index]
            tmpcustomer.change_firstname(ap_firstname)
            tmpcustomer.change_lastname(ap_lastname)
            tmpcustomer.change_mobile(ap_mobile)
            tmpcustomer.change_email(ap_email)
            clear_content_frame(content_frame)
            label = ttk.Label(content_frame, text="Ο πελατης ενημερωθηκε επιτυχως.\n" + str(tmpcustomer))
            label.pack(fill=tk.X, padx=5, pady=5)

        def display_customer_info():
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

        # # label
        label = ttk.Label(content_frame, text="Επιλεξτε πελατη:")
        label.pack(fill=tk.X, padx=5, pady=5)

        # create a combobox
        selected_customer = tk.StringVar()
        customer_cb = ttk.Combobox(content_frame, textvariable=selected_customer)

        customer_cb['values'] = [customers_list[m] for m in range(len(customers_list))]

        # prevent typing a value
        customer_cb['state'] = 'readonly'

        # place the widget
        customer_cb.pack(fill=tk.X, padx=5, pady=5)

        customer_cb.bind("<<ComboboxSelected>>", lambda _: display_customer_info())

        # label
        label = ttk.Label(content_frame, text="Ονομα:")
        label.pack(fill=tk.X, padx=5, pady=5)

        textbox_firstname = tk.Text(content_frame, height=1, width=10)
        textbox_firstname.pack(fill=tk.X, padx=5, pady=5)

        label = ttk.Label(content_frame, text="Επωνυμο:")
        label.pack(fill=tk.X, padx=5, pady=5)

        textbox_lastname = tk.Text(content_frame, height=1, width=10)
        textbox_lastname.pack(fill=tk.X, padx=5, pady=5)

        label = ttk.Label(content_frame, text="Τηλεφωνο:")
        label.pack(fill=tk.X, padx=5, pady=5)

        textbox_phone = tk.Text(content_frame, height=1, width=10)
        textbox_phone.pack(fill=tk.X, padx=5, pady=5)

        label = ttk.Label(content_frame, text="Email:")
        label.pack(fill=tk.X, padx=5, pady=5)

        textbox_email = tk.Text(content_frame, height=1, width=10)
        textbox_email.pack(fill=tk.X, padx=5, pady=5)

        btn_frame = tk.Frame(content_frame)
        btn_frame.configure(bg= "#282830")
        btn_frame.pack(anchor=tk.N, expand=True, side=tk.LEFT)

        ok_btn = tk.Button(btn_frame, text="Ενημερωση", command=lambda: retrieve_input())
        ok_btn.grid(row=0,column=0,padx=10)
        cancel_btn = tk.Button(btn_frame, text="Ακυρωση", command=lambda: clear_content_frame(content_frame))
        cancel_btn.grid(row=0,column=1)


    def delete_customer_clicked(event=None):
        clear_content_frame(content_frame)

        from customers import Customer
        customers_list = Customer.get_table_rows()

        def retrieve_input():
            customer_cb_selected_index = customer_cb.current()
            if(customer_cb_selected_index == -1):
                return

            if(not tk.messagebox.askokcancel("Προσοχη!", "Προσοχη! \nΕχετε επιλεξει να διαγραψετε τον πελατη\n\n"
                                         +str(customers_list[customer_cb_selected_index])+
                                         "\n\nΘα διαγραφουν μαζι και ολα του τα ραντεβου."
                                         "\nΕιστε σιγουροι;")):
                return

            customerIDs = {}
            counter = 0
            for customer in customers_list:
                customerIDs[counter] = customer.id
                counter = counter + 1

            from customers import delete_appointments_of_customerid
            delete_appointments_of_customerid(customerIDs[customer_cb_selected_index])
            tmpcustomer = customers_list[customer_cb_selected_index]
            tmpcustomer.delete()

            clear_content_frame(content_frame)
            label = ttk.Label(content_frame,
                              text="Ο πελατης διαγραφηκε επιτυχως.\n" + str(customers_list[customer_cb_selected_index]))
            label.pack(fill=tk.X, padx=5, pady=5)

        # label
        label = ttk.Label(content_frame, text="Επιλεξτε πελατη:")
        label.pack(fill=tk.X, padx=5, pady=5)

        # create a combobox
        selected_customer = tk.StringVar()
        customer_cb = ttk.Combobox(content_frame, textvariable=selected_customer)

        customer_cb['values'] = [customers_list[m] for m in range(len(customers_list))]

        # prevent typing a value
        customer_cb['state'] = 'readonly'

        # place the widget
        customer_cb.pack(fill=tk.X, padx=5, pady=5)


        btn_frame = tk.Frame(content_frame)
        btn_frame.configure(bg= "#282830")
        btn_frame.pack(anchor=tk.N, expand=True, side=tk.LEFT)

        ok_btn = tk.Button(btn_frame, text="Διαγραφη", command=lambda: retrieve_input())
        ok_btn.grid(row=0,column=0,padx=10)
        cancel_btn = tk.Button(btn_frame, text="Ακυρωση", command=lambda: clear_content_frame(content_frame))
        cancel_btn.grid(row=0,column=1)


    def new_appointment_clicked(event=None):
        clear_content_frame(content_frame)

        from customers import Customer
        customers_list = Customer.get_table_rows()

        def retrieve_input():
            customer_cb_selected_index = customer_cb.current()
            if(customer_cb_selected_index == -1):
                return

            from customers import Customer
            from appointments import Appointment, no_overlapping_appointments

            customerIDs = {}
            counter = 0
            for customer in customers_list:
                customerIDs[counter] = customer.id
                counter = counter + 1

            ap_customerid = customerIDs[customer_cb_selected_index]
            ap_datetime = str(cal.get()) + ' ' + str(hour_cb.get()) + ':' + str(minutes_cb.get())
            ap_duration = duration_cb.get()
            # print(ap_customerid)
            # print(ap_datetime)
            # print(ap_duration)

            if(not no_overlapping_appointments(ap_datetime, ap_duration)):
                tk.messagebox.showerror("Λαθος Εισοδος", "Ο συνδιασμος ημερομηνιας/ωρας και διαρκειας "
                                            "\nπου βαλατε ειναι ηδη δεσμευμενος απο αλλο ραντεβου."
                                            "\nΔοκιμαστε παλι.")
                return

            newappointment = Appointment.create(ap_customerid, ap_datetime, ap_duration)
            clear_content_frame(content_frame)
            label = ttk.Label(content_frame, text="Το ραντεβου δημιουργηθηκε επιτυχως.\n" + str(newappointment))
            label.pack(fill=tk.X, padx=5, pady=5)

        # label
        label = ttk.Label(content_frame, text="Επιλεξτε πελατη:")
        label.pack(fill=tk.X, padx=5, pady=5)

        # create a combobox
        selected_customer = tk.StringVar()
        customer_cb = ttk.Combobox(content_frame, textvariable=selected_customer)

        customer_cb['values'] = [customers_list[m] for m in range(len(customers_list))]

        # prevent typing a value
        customer_cb['state'] = 'readonly'

        # place the widget
        customer_cb.pack(fill=tk.X, padx=5, pady=5)

        # label
        label = ttk.Label(content_frame, text="Επιλεξτε Ημερομηνια:")
        label.pack(fill=tk.X, padx=5, pady=5)

        from tkcalendar import DateEntry
        cal = DateEntry(content_frame, locale='en_US', date_pattern='YYYY-mm-dd',
                        width=12, year=datetime.now().year, month=datetime.now().month, day=datetime.now().day,
                        borderwidth=2)

        cal.pack(fill=tk.X, padx=5, pady=5)

        # label
        label = ttk.Label(content_frame, text="Επιλεξτε Ωρα:")
        label.pack(fill=tk.X, padx=5, pady=5)

        hour_cb = ttk.Combobox(content_frame)
        hours_list = [*range(0, 24)]
        hour_cb['values'] = [str(element).rjust(2,'0') for element in hours_list]

        hour_cb.current(datetime.now().hour)
        # prevent typing a value
        hour_cb['state'] = 'readonly'
        # place the widget
        hour_cb.pack(fill=tk.X, padx=5, pady=5)

        # label
        minutes_cb = ttk.Combobox(content_frame)
        minites_int_list = [*range(0, 60)]
        minutes_cb['values'] = [str(element).rjust(2,'0') for element in minites_int_list]

        minutes_cb.current(datetime.now().minute)

        # prevent typing a value
        minutes_cb['state'] = 'readonly'

        # place the widget
        minutes_cb.pack(fill=tk.X, padx=5, pady=5)

        # label
        label = ttk.Label(content_frame, text="Επιλεξτε Διαρκεια:")
        label.pack(fill=tk.X, padx=5, pady=5)

        # selected_duration = tk.StringVar()
        duration_cb = ttk.Combobox(content_frame)

        duration_cb['values'] = [5, 10, 15, 30, 60, 90, 120]

        duration_cb.current(3)

        # prevent typing a value
        duration_cb['state'] = 'readonly'

        # place the widget
        duration_cb.pack(fill=tk.X, padx=5, pady=5)

        btn_frame = tk.Frame(content_frame)
        btn_frame.configure(bg= "#282830")
        btn_frame.pack(anchor=tk.N, expand=True, side=tk.LEFT)

        ok_btn = tk.Button(btn_frame, text="Δημιουργια", command=lambda: retrieve_input())
        ok_btn.grid(row=0,column=0,padx=10)
        cancel_btn = tk.Button(btn_frame, text="Ακυρωση", command=lambda: clear_content_frame(content_frame))
        cancel_btn.grid(row=0,column=1)


    def modify_appointment_clicked(event=None):
        clear_content_frame(content_frame)

        from customers import Customer
        customers_list = Customer.get_table_rows()

        from appointments import list_appointments_with_customer_fullname, Appointment, no_overlapping_appointments
        appointments_tablerows = list_appointments_with_customer_fullname()
        appointments_list = Appointment.get_table_rows()

        def retrieve_input():
            appointment_cb_selected_index = appointment_cb.current()
            if(appointment_cb_selected_index == -1):
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
            # print(ap_customerid)
            # print(ap_datetime)
            # print(ap_duration)

            if(not no_overlapping_appointments(ap_datetime, ap_duration)):
                tk.messagebox.showerror("Λαθος Εισοδος", "Ο συνδιασμος ημερομηνιας/ωρας και διαρκειας "
                                            "\nπου βαλατε ειναι ηδη δεσμευμενος απο αλλο ραντεβου."
                                            "\nΔοκιμαστε παλι.")
                return

            tmpappointment = appointments_list[appointment_cb_selected_index]
            # print(tmpappointment)
            tmpappointment.change_customerid(ap_customerid)
            tmpappointment.change_datetime(ap_datetime)
            tmpappointment.change_duration(ap_duration)
            # print(tmpappointment)

            clear_content_frame(content_frame)
            label = ttk.Label(content_frame, text="Το ραντεβου ενημερωθηκε επιτυχως.\n" + str(tmpappointment))
            label.pack(fill=tk.X, padx=5, pady=5)

        def display_appointment_info():
            appointment_cb_selected_index = appointment_cb.current()
            tmpappointment = appointments_list[appointment_cb_selected_index]

            customerIDs = {}
            counter = 0
            for customer in customers_list:
                customerIDs[customer.id] = counter
                counter = counter + 1

            ap_customerid = customerIDs[tmpappointment.customerid]

            # print('Customer')
            # print(ap_customerid)
            # print(customerIDs)
            # print('')

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

            # print('Date')
            # print(datetime_obj.date())
            # print(datetime_obj.hour)
            # print(datetime_obj.minute)
            # print('')

            cal.set_date(datetime_obj.date())


            durationIndex = {}
            counter = 0
            for value in duration_cb['values']:
                durationIndex[int(value)] = counter
                counter = counter + 1

            # print('Duration')
            # print(durationIndex)
            # print(tmpappointment.duration)
            # print(durationIndex[tmpappointment.duration])
            # print('')

            duration_cb.current(durationIndex[tmpappointment.duration])

        # label
        label = ttk.Label(content_frame, text="Επιλεξτε ρεντεβου:")
        label.pack(fill=tk.X, padx=5, pady=5)

        # create a combobox
        #selected_appointment = tk.StringVar()
        appointment_cb = ttk.Combobox(content_frame)

        appointment_cb['values'] = [appointments_tablerows[m] for m in range(len(appointments_tablerows))]

        # prevent typing a value
        appointment_cb['state'] = 'readonly'

        # place the widget
        appointment_cb.pack(fill=tk.X, padx=5, pady=5)

        # label
        label = ttk.Label(content_frame, text="Επιλεξτε πελατη:")
        label.pack(fill=tk.X, padx=5, pady=5)

        # create a combobox
        #selected_customer = tk.StringVar()
        customer_cb = ttk.Combobox(content_frame)

        customer_cb['values'] = [customers_list[m] for m in range(len(customers_list))]

        # prevent typing a value
        customer_cb['state'] = 'readonly'

        # place the widget
        customer_cb.pack(fill=tk.X, padx=5, pady=5)

        # label
        label = ttk.Label(content_frame, text="Επιλεξτε Ημερομηνια:")
        label.pack(fill=tk.X, padx=5, pady=5)

        cal = DateEntry(content_frame, locale='en_US', date_pattern='YYYY-mm-dd',
                        width=12, year=datetime.now().year, month=datetime.now().month, day=datetime.now().day,
                        borderwidth=2)

        cal.pack(fill=tk.X, padx=5, pady=5)

        # label
        label = ttk.Label(content_frame, text="Επιλεξτε Ωρα:")
        label.pack(fill=tk.X, padx=5, pady=5)

        hour_cb = ttk.Combobox(content_frame)
        hours_list = [*range(0, 24)]
        hour_cb['values'] = [str(element).rjust(2,'0') for element in hours_list]

        hour_cb.current(datetime.now().hour)

        # prevent typing a value
        hour_cb['state'] = 'readonly'

        # place the widget
        hour_cb.pack(fill=tk.X, padx=5, pady=5)

        # label
        minutes_cb = ttk.Combobox(content_frame)
        minites_int_list = [*range(0, 60)]
        minutes_cb['values'] = [str(element).rjust(2,'0') for element in minites_int_list]
        minutes_cb.current(datetime.now().minute)

        # prevent typing a value
        minutes_cb['state'] = 'readonly'

        # place the widget
        minutes_cb.pack(fill=tk.X, padx=5, pady=5)

        # label
        label = ttk.Label(content_frame, text="Επιλεξτε Διαρκεια:")
        label.pack(fill=tk.X, padx=5, pady=5)

        # selected_duration = tk.StringVar()
        duration_cb = ttk.Combobox(content_frame)

        duration_cb['values'] = [5, 10, 15, 30, 60, 90, 120]

        duration_cb.current(3)

        # prevent typing a value
        duration_cb['state'] = 'readonly'

        # place the widget
        duration_cb.pack(fill=tk.X, padx=5, pady=5)

        appointment_cb.bind("<<ComboboxSelected>>", lambda _: display_appointment_info())

        btn_frame = tk.Frame(content_frame)
        btn_frame.configure(bg= "#282830")
        btn_frame.pack(anchor=tk.N, expand=True, side=tk.LEFT)

        ok_btn = tk.Button(btn_frame, text="Ενημερωση", command=lambda: retrieve_input())
        ok_btn.grid(row=0,column=0,padx=10)
        cancel_btn = tk.Button(btn_frame, text="Ακυρωση", command=lambda: clear_content_frame(content_frame))
        cancel_btn.grid(row=0,column=1)


    def delete_appointment_clicked(event=None):
        clear_content_frame(content_frame)

        from appointments import list_appointments_with_customer_fullname, Appointment
        appointments_tablerows = list_appointments_with_customer_fullname()
        appointments_list = Appointment.get_table_rows()
        appointmentIDs = {}

        def retrieve_input():
            appointment_cb_selected_index = appointment_cb.current()
            if(appointment_cb_selected_index == -1):
                return

            if(not tk.messagebox.askokcancel("Προσοχη!", "Προσοχη! \nΕχετε επιλεξει να διαγραψετε το ραντεβου\n\n"
                                         +str(appointments_list[appointment_cb_selected_index])+
                                         "\n\nΕιστε σιγουροι;")):
                return

            counter = 0
            for appointment in appointments_list:
                appointmentIDs[counter] = appointment.id
                counter = counter + 1

            tmpappointment = appointments_list[appointment_cb_selected_index]
            tmpappointment.delete()

            clear_content_frame(content_frame)
            label = ttk.Label(content_frame, text="Το ραντεβου διαγραφηκε επιτυχως.\n" + str(
                appointments_list[appointment_cb_selected_index]))
            label.pack(fill=tk.X, padx=5, pady=5)

        # label
        label = ttk.Label(content_frame, text="Επιλεξτε ρεντεβου:")
        label.pack(fill=tk.X, padx=5, pady=5)

        # create a combobox
        selected_appointment = tk.StringVar()
        appointment_cb = ttk.Combobox(content_frame, textvariable=selected_appointment)

        appointment_cb['values'] = [appointments_tablerows[m] for m in range(len(appointments_tablerows))]

        # prevent typing a value
        appointment_cb['state'] = 'readonly'

        # place the widget
        appointment_cb.pack(fill=tk.X, padx=5, pady=5)

        btn_frame = tk.Frame(content_frame)
        btn_frame.configure(bg= "#282830")
        btn_frame.pack(anchor=tk.N, expand=True, side=tk.LEFT)

        ok_btn = tk.Button(btn_frame, text="Διαγραφη", command=lambda: retrieve_input())
        ok_btn.grid(row=0,column=0,padx=10)
        cancel_btn = tk.Button(btn_frame, text="Ακυρωση", command=lambda: clear_content_frame(content_frame))
        cancel_btn.grid(row=0,column=1)

    def search_by_date_gui():
     def search_and_show_results():
        date = cal.get_date()
        if date:
            #formatted_date = date.strftime('YYYY-MM-DD')
            results = search_by_date(date)
            if results:
                show_results_window(results)
            else:
                messagebox.showinfo("No Results", "No results found.")
              
     clear_content_frame(content_frame)

     label_date = tk.Label(content_frame, text="Παρακαλω επιλεξτε Ημερομηνία:")
     label_date.pack(padx=5,pady=5)
     cal = DateEntry(content_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
     cal.pack(fill=tk.X, padx=5, pady=5)

     button_search = tk.Button(content_frame, text="Αναζήτηση", command=search_and_show_results)
     button_search.pack(pady=5)

    # button_return = tk.Button(content_frame, text="Επιστροφή στο Μενού Αναζήτησης", command=lambda: return_to_main_menu(main_menu, content_frame))
    # button_return.pack(pady=5)


    def search_by_email_gui():
      clear_content_frame(content_frame)
      def search_and_show_results():
        email = entry_email.get()
        if email:
            results = search_by_customer_email(email)
            if results:
                show_results_window(results)
            else:
                messagebox.showinfo("No Results", "Δεν βρέθηκαν αποτελέσματα.")
 
      label_email = tk.Label(content_frame, text="Παρακαλώ εισάγετε το email του πελάτη:")
      label_email.pack(padx=5,pady=5)
      entry_email = tk.Entry(content_frame)
      entry_email.pack(fill=tk.X, padx=5, pady=5)

      button_search = tk.Button(content_frame, text="Αναζήτηση", command=search_and_show_results)
      button_search.pack(pady=5)

      #button_return = tk.Button(content_frame, text="Επιστροφή στο Μενού Αναζήτησης", command=lambda: return_to_main_menu(main_menu, content_frame))
      #button_return.pack(pady=5)

      

    def show_results_window(results):
      def export_to_excel_window():
        nonlocal button_export_excel
        button_export_excel.destroy()
        def export():
            filename = entry_filename.get()
            if filename:

                export_to_excel(results, filename + ".xlsx")
                                
                
        label_filename = tk.Label(content_frame, text="Πληκτολογείστε το ονομα αρχείου Excel (χωρις κατάληξη):")
        label_filename.pack()

        entry_filename = tk.Entry(content_frame)
        entry_filename.pack()

        button_export = tk.Button(content_frame, text="Εξαγωγή", command=export)
        button_export.pack()   
    
      headers = ("Κωδικός", "Όνομα", "Επίθετο", "Ημερομηνία/Ώρα Ραντεβού", "Διάρκεια")

      frame = customtkinter.CTkScrollableFrame(content_frame)
      frame.pack(padx=10, pady=10,fill=tk.BOTH, expand=True)

      frame.config(width=815)


      # Προσθήκη κεφαλίδων
      for col, header in enumerate(headers):
        label_header = tk.Label(frame, text=header, font=("Helvetica", 10, "bold"), padx=10, pady=5, relief=tk.RIDGE)
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
      button_export_excel.pack(pady=5)
    

    def new_file_clicked():
         print("placeholder")


    root = tk.Tk()
    root.title("Διαχειρηση Ραντεβου - Project07")
    root.geometry("815x630")
    menubar = tk.Menu()

    tk_search_by_date = tk.Menu(menubar, tearoff=False)
    tk_search_by_date.add_command(
        label="Με Ημερομηνια",
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
        label="Δημιουργια",
        command=new_customer_clicked,
        compound=tk.LEFT
    )
    tk_customers_menu.add_command(
        label="Τροποποιηση",
        command=modify_customer_clicked,
        compound=tk.LEFT
    )
    tk_customers_menu.add_command(
        label="Διαγραφη",
        command=delete_customer_clicked,
        compound=tk.LEFT
    )

    tk_appointments_menu = tk.Menu(menubar, tearoff=False)
    tk_appointments_menu.add_command(
        label="Δημιουργια",
        command=new_appointment_clicked,
        compound=tk.LEFT
    )
    tk_appointments_menu.add_command(
        label="Τροποποιηση",
        command=modify_appointment_clicked,
        compound=tk.LEFT
    )
    tk_appointments_menu.add_command(
        label="Διαγραφη",
        command=delete_appointment_clicked,
        compound=tk.LEFT
    )

    tk_appointments_menu.add_separator()

    tk_appointments_menu.add_cascade(
        menu=tk_search_by_date,
        label="Αναζητηση"
    )

    tk_appointments_menu.add_command(
        label="Υπενθυμιση",
        command=new_file_clicked,
        compound=tk.LEFT
    )
    tk_appointments_menu.add_command(
        label="Εκτυπωση",
        command=new_file_clicked,
        compound=tk.LEFT
    )

    tk_settings_menu = tk.Menu(menubar, tearoff=False)

    menubar.add_cascade(menu=tk_customers_menu, label="Πελατες")
    menubar.add_cascade(menu=tk_appointments_menu, label="Ραντεβου")
    menubar.add_cascade(menu=tk_settings_menu, label="Ρυθμισεις")

    root.config(menu=menubar,bg= "#282830")

    icon = tk.PhotoImage(file="WindowLogo.png")
    root.iconphoto(True, icon)
    root.title("Διαχείρηση Ραντεβού")


    content_frame = tk.Frame(root,bg= "#282830")  # , bg="orange")
    content_frame.pack(anchor=tk.N, fill=tk.BOTH, expand=True, side=tk.LEFT)
  
    logo_photo = load_logo(scale_factor=0.5)  # Φορτώνουμε το λογότυπο
    if logo_photo:
        label_logo = tk.Label(root, image=logo_photo,bg= "#282830")
        label_logo.pack(side=tk.BOTTOM)


    root.mainloop()