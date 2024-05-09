import appointments_menu
import customers_menu
import search_menu
import print_menu
from reminder import send_appointment_reminder

def change_frame(old_content, old_title):
    # Destroy old content and display new content
    old_content.destroy()
    old_title.destroy()

def open_appointments_menu():
    # Implement function to open appointments menu
    pass

def sidebar(window):
    # Create sidebar frame with buttons
    sidebar_frame = tk.Frame(window, bg="#156fed", width=200)
    sidebar_frame.pack(side="left", fill="y")

    button1 = tk.Label(sidebar_frame, text="Manage Customers", fg="white", bg="#156fed", cursor="hand2", 
                   font=("Commissioner", 12), padx=10, pady=5)
    button1.pack(pady=10)
    button1.bind("<Button-1>", lambda event: change_frame(search_widget, search_frame))

    button2 = tk.Label(sidebar_frame, text="Manage Appointments", fg="white", bg="#156fed", cursor="hand2",
                   font=("Commissioner", 12), padx=10, pady=5)
    button2.pack(pady=10)
    button2.bind("<Button-1>", lambda event: open_appointments_menu())

    return sidebar_frame


def create_search_widget(window):
    # Create search widget
    search_frame = tk.Frame(window, height=50)
    search_frame.pack(side="top", fill="x")

    search_label = tk.Label(search_frame, text="Find customer", fg="#000000", font=("Commissioner", 22), padx=10, pady=5)
    search_label.pack(side="left")

    # Assuming search.create_search_widget() returns the widgets you mentioned
    search_widget, entry, button = search.create_search_widget(search_frame)
    search_widget.pack()

    return search_frame, search_widget

# Initialize main window
window = tk.Tk()
window.title("Appointment app")
window.configure(bg="#f0f0f0")  # Light gray
window.geometry("800x600")

# Create sidebar
sidebar_frame = sidebar(window)

# Create main content frame
main_content = tk.Frame(window, bg="#f0f0f0")
main_content.pack(side="right", fill="both", expand=True)

# Create search widget
search_frame, search_widget = create_search_widget(window)

# Run the application
window.mainloop()
