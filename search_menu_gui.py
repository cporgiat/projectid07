import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from search import search_by_date, search_by_customer_email, print_results, export_to_excel

def load_logo(scale_factor=0.5):
    try:
        logo = tk.PhotoImage(file="Logo.png")
        logo = logo.subsample(int(1/scale_factor))  # Κλιμάκωση του λογότυπου
        return logo
    except tk.TclError as e:
        messagebox.showerror("Error", f"Failed to load logo: {e}")
        return None

def return_to_main_menu(main_menu_function, window):
    main_menu_function(window)
def search_by_date_gui(main_window):
    def search_and_show_results():
        date = cal.get_date()
        if date:
            formatted_date = date.strftime('YYYY-MM-DD')
            results = search_by_date(formatted_date)
            if results:
                window.destroy()
                show_results_window(results)
            else:
                messagebox.showinfo("No Results", "No results found.")
                main_menu(window)  # Καλούμε το main_menu με το αρχικό παράθυρο


    main_window.destroy()

    window = tk.Tk()
    window.title("Αναζήτηση με Ημερομηνία")
    label_date = tk.Label(window, text="Παρακαλω επιλεξτε Ημερομηνία:")
    label_date.pack()
    cal = DateEntry(window, width=12, background='darkblue', foreground='white', borderwidth=2)
    cal.pack(pady=10)

    button_search = tk.Button(window, text="Αναζήτηση", command=search_and_show_results)
    button_search.pack(pady=5)

    button_return = tk.Button(window, text="Επιστροφή στο Μενού Αναζήτησης", command=lambda: return_to_main_menu(main_menu, window))
    button_return.pack(pady=5)

    logo_photo = load_logo(scale_factor=0.2)  # Φορτώνουμε το λογότυπο
    if logo_photo:
        label_logo = tk.Label(window, image=logo_photo)
        label_logo.pack(pady=10)

    window.mainloop()


def search_by_email_gui(main_window):
    def search_and_show_results():
        email = entry_email.get()
        if email:
            results = search_by_customer_email(email)
            if results:
                window.destroy()
                show_results_window(results)
            else:
                messagebox.showinfo("No Results", "Δεν βρέθηκαν αποτελέσματα.")
                main_menu(window)  # Καλούμε το main_menu με το αρχικό παράθυρο

    main_window.destroy()

    window = tk.Tk()
    window.title("Αναζήτηση με E-mail")
    window.geometry("400x300")

    label_email = tk.Label(window, text="Παρακαλώ εισάγετε το email του πελάτη:")
    label_email.pack()
    entry_email = tk.Entry(window)
    entry_email.pack()

    button_search = tk.Button(window, text="Αναζήτηση", command=search_and_show_results)
    button_search.pack(pady=5)

    button_return = tk.Button(window, text="Επιστροφή στο Μενού Αναζήτησης", command=lambda: return_to_main_menu(main_menu, window))
    button_return.pack(pady=5)

    logo_photo = load_logo(scale_factor=0.2)  # Φορτώνουμε το λογότυπο
    if logo_photo:
        label_logo = tk.Label(window, image=logo_photo)
        label_logo.pack(pady=10)

    window.mainloop()


def show_results_window(results):
    def export_to_excel_window():
        def export():
            filename = entry_filename.get()
            if filename:
                export_to_excel(results, filename + ".xlsx")
                window.destroy()

        window = tk.Tk()
        window.title("Εξαγωγή σε Excel")

        label_filename = tk.Label(window, text="Πληκτολογείστε το ονομα αρχείου Excel (χωρις κατάληξη):")
        label_filename.pack()

        entry_filename = tk.Entry(window)
        entry_filename.pack()

        button_export = tk.Button(window, text="Εξαγωγή", command=export)
        button_export.pack()

        window.mainloop()

    window = tk.Tk()
    window.title("Αποτελέσματα Αναζήτησης")

    headers = ("Κωδικός", "Όνομα", "Επίθετο", "Ημερομηνία/Ώρα Ραντεβού", "Διάρκεια")

    frame = tk.Frame(window)
    frame.pack(padx=10, pady=10)

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

    button_export_excel = tk.Button(window, text="Εξαγωγή σε Excel", command=export_to_excel_window)
    button_export_excel.pack(pady=5)

    button_return = tk.Button(window, text="Επιστρογή στο Μενου Αναζήτησης", command=lambda: main_menu(window))
    button_return.pack(pady=5)

    window.mainloop()


def main_menu(previous_window=None):
    if previous_window:
        previous_window.destroy()

    window = tk.Tk()
    window.title("Διαχείρηση Ραντεβού")
    window.geometry("800x600")

    label_menu = tk.Label(window, text="Μενού Αναζήτησης", font=("Helvetica", 22))
    label_menu.pack(pady=20)

    button_search_date = tk.Button(window, text="Αναζήτηση με Ημερομηνία", font=("Helvetica", 12),
                                    command=lambda: search_by_date_gui(window))
    button_search_date.pack(pady=5)

    button_search_email = tk.Button(window, text="Αναζήτηση με Email", font=("Helvetica", 12),
                                     command=lambda: search_by_email_gui(window))
    button_search_email.pack(pady=5)




    button_exit = tk.Button(window, text="Επιστροφή στο Κύριο Μενού", font=("Helvetica", 12), command=window.quit)
    button_exit.pack(pady=20)

    logo_photo = load_logo(scale_factor=0.5)  # Φορτώνουμε το λογότυπο
    if logo_photo:
        label_logo = tk.Label(window, image=logo_photo)
        label_logo.pack(pady=10)


    window.mainloop()



if __name__ == "__main__":
    main_menu()
