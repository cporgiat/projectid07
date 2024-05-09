from tkinter import *

def create_search_widget(parent):
    search_widget = Frame(parent)
    
    label1 = Label(search_widget, text="Αναζήτηση")
    label1.grid(row=0, column=0)

    entry = Entry(search_widget, width=30)
    entry.grid(row=0, column=1)

    def search():
        search_term = entry.get()  # Get the text entered in the entry widget
        # Perform the search operation using the search term (you can replace this with your actual search logic)
        print("Searching for:", search_term)

    button = Button(search_widget, text="Search", command=search)
    button.grid(row=0, column=2, pady=10)

    return search_widget, entry, button
