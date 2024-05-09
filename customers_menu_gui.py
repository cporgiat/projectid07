import tkinter as tk
import customers_menu

class DataEntryFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.create_user_info_widgets()

    def create_user_info_widgets(self):
        # User Information Frame
        self.user_info_frame = tk.LabelFrame(self, text="User Information")
        self.user_info_frame.grid(row=0, column=0, padx=20, pady=20)

        # Labels
        first_name_label = tk.Label(self.user_info_frame, text="First Name")
        first_name_label.grid(row=0, column=0)
        last_name_label = tk.Label(self.user_info_frame, text="Last Name")
        last_name_label.grid(row=0, column=1)
        phone_label = tk.Label(self.user_info_frame, text="Phone")
        phone_label.grid(row=2, column=0)
        email_label = tk.Label(self.user_info_frame, text="Email")
        email_label.grid(row=2, column=1)

        # Entry boxes
        self.first_name_entry = tk.Entry(self.user_info_frame)
        self.last_name_entry = tk.Entry(self.user_info_frame)
        self.phone_entry = tk.Entry(self.user_info_frame)
        self.email_entry = tk.Entry(self.user_info_frame)
        self.first_name_entry.grid(row=1, column=0)
        self.last_name_entry.grid(row=1, column=1)
        self.phone_entry.grid(row=3, column=0)
        self.email_entry.grid(row=3, column=1)

        # Stylize boxes
        for widget in self.user_info_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        # Button
        button = tk.Button(self, text="Enter data", command=self.menu_customer_create)
        button.grid(row=1, column=0, sticky="news", padx=20, pady=10)

    def menu_customer_create(self):
        ap_firstname = self.first_name_entry.get()
        ap_lastname = self.last_name_entry.get()
        ap_mobile = self.phone_entry.get()
        ap_email = self.email_entry.get()
        newcustomer = customers_menu.menu_customer_create(ap_firstname, ap_lastname, ap_mobile, ap_email)
        print(newcustomer)

class EditFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # Create/Edit Frame
        self.edit_label = tk.Label(self, text="Edit Frame")
        self.edit_label.pack()

class DeleteFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.display_customer_info_widgets()    

    def display_customer_info_widgets(self):
        for customer_id, customer_info in customers_menu.customers.items():  # Use .items() to iterate over key-value pairs
            customer_str = f"ID: {customer_id}, Name: {customer_info['Name']}, Last Name: {customer_info['LastName']}, Phone: {customer_info['Phone']}, Email: {customer_info['Email']}"
            label = tk.Label(self, text=customer_str)
            label.pack()

def switch_frame(old_frame, new_frame):
    old_frame.destroy()
    new_frame.pack()

def main():
    window = tk.Tk()
    window.title("Data Entry Form")

    CustomerFrame = tk.Frame(window)
    CustomerFrame.pack()

    # First button
    button1 = tk.Button(CustomerFrame, text="Εισαγωγή Νέου Χρήστη", command=lambda: switch_frame(CustomerFrame, data_entry_frame))
    button1.grid(row=0, column=0, sticky="news", padx=20, pady=10)

    # Create DataEntryFrame instance
    data_entry_frame = DataEntryFrame(window)

    # Second button
    button2 = tk.Button(CustomerFrame, text="Επεξεργασία Χρήστη", command=lambda: switch_frame(CustomerFrame, edit_frame))
    button2.grid(row=0, column=1, sticky="news", padx=20, pady=10)

    # Create EditFrame instance
    edit_frame = EditFrame(window)

    # Third button
    button3 = tk.Button(CustomerFrame, text="Διαγραφή Χρήστη", command=lambda: switch_frame(CustomerFrame, delete_frame))
    button3.grid(row=0, column=2, sticky="news", padx=20, pady=10)

    # Create DeleteFrame instance
  #  delete_frame = DeleteFrame(window)



    window.mainloop()

if __name__ == "__main__":
    main()