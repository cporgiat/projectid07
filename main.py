import appointments_menu
import customers_menu
import search_menu
import print_menu
from utils import get_number
from reminder import send_appointment_reminder


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

        choice = get_number("Επιλογη: ")

        if choice == '1':
            customers_menu.menu_customer()
        elif choice == '2':
            appointments_menu.menu_appointment()
        elif choice == '3':
            search_menu.search_menu()
        elif choice == '4':
            date = input("Εισάγετε την ημερομηνία για την οποία θέλετε να στείλετε υπενθυμίσεις (YYYY-MM-DD): ")
            send_appointment_reminder(date)
        elif choice == '5':
            print_menu.print_menu()
        elif choice == '98':
            settings_menu.menu_settings()
        elif choice == '99':
            print("Εξοδος απο το προγραμμα")
            break
        else:
            print("Λαθος επιλογη. Παρακαλω επιλεξτε παλι.")


if __name__ == '__main__':
    import tkinter as tk
    from tkinter import ttk

    from calendar import month_name
    from datetime import datetime


    def new_customer_clicked(event=None):
        print("new_customer_clicked was clicked!")
        for widget in content_frame.winfo_children():
            widget.destroy()

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

        ok_btn = tk.Button(content_frame, text="Δημιουργια")
        ok_btn.pack()

    def new_appointment_clicked(event=None):
        print("new_appointment_clicked was clicked!")
        for widget in content_frame.winfo_children():
            widget.destroy()

        # label
        label = ttk.Label(content_frame, text="Please select date:")
        label.pack(fill=tk.X, padx=5, pady=5)

        from tkcalendar import DateEntry
        cal = DateEntry(content_frame,locale='en_US', date_pattern='YYYY-mm-dd',
                        width=12, year=datetime.now().year, month=datetime.now().month, day=datetime.now().day,
                         borderwidth=2)

        cal.pack(fill=tk.X, padx=5, pady=5)

        # label
        label = ttk.Label(content_frame, text="Please select time:")
        label.pack(fill=tk.X, padx=5, pady=5)

        from tktimepicker import SpinTimePickerOld, constants
        time_picker = SpinTimePickerOld(content_frame)
        time_picker.addAll(constants.HOURS24)
        time_picker.pack(fill=tk.X, padx=5, pady=5)

        ok_btn = tk.Button(content_frame, text="Δημιουργια")
        ok_btn.pack()

        # # label
        # label = ttk.Label(content_frame, text="Please select month:")
        # label.pack(fill=tk.X, padx=5, pady=5)
        #
        # # create a combobox
        # selected_month = tk.StringVar()
        # month_cb = ttk.Combobox(content_frame, textvariable=selected_month)
        #
        # # get first 3 letters of every month name
        # month_cb['values'] = [month_name[m][0:3] for m in range(1, 13)]
        #
        # # prevent typing a value
        # month_cb['state'] = 'readonly'
        #
        # # place the widget
        # month_cb.pack(fill=tk.X, padx=5, pady=5)

    def new_file_clicked():
        print("placeholder")


    root = tk.Tk()
    root.title("Διαχειρηση Ραντεβου - Project07")
    root.geometry("400x300")
    menubar = tk.Menu()

    tk_search_by_date = tk.Menu(menubar, tearoff=False)
    tk_search_by_date.add_command(
        label="Με Ημερομηνια",
        command=new_file_clicked,
        compound=tk.LEFT
    )
    tk_search_by_date.add_command(
        label="Με email",
        command=new_file_clicked,
        compound=tk.LEFT
    )
    tk_search_by_date.add_command(
        label="Με τηλεφωνο",
        command=new_file_clicked,
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
        command=new_file_clicked,
        compound=tk.LEFT
    )
    tk_customers_menu.add_command(
        label="Διαγραφη",
        command=new_file_clicked,
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
        command=new_file_clicked,
        compound=tk.LEFT
    )
    tk_appointments_menu.add_command(
        label="Διαγραφη",
        command=new_file_clicked,
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

    root.config(menu=menubar)

    content_frame = tk.Frame(root) #, bg="orange")
    content_frame.pack(anchor=tk.N, fill=tk.BOTH, expand=True, side=tk.LEFT)

    root.mainloop()
