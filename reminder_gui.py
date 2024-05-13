import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from search import search_by_date  # Εισαγωγή από το προηγούμενο αρχείο
import tkcalendar

def send_email(to_address, subject, body, from_address='your_email@example.com', smtp_server='smtp.example.com',
               smtp_port=587, smtp_user='username', smtp_pass='password'):
    # Δημιουργία του email
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject

    # Προσθέτουμε το σώμα του email
    msg.attach(MIMEText(body, 'plain'))

    # Ρύθμιση και αποστολή του email μέσω SMTP
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Κρυπτογράφηση της σύνδεσης
        server.login(smtp_user, smtp_pass)  # Σύνδεση στον SMTP server
        server.sendmail(from_address, to_address, msg.as_string())  # Αποστολή email
        server.quit()  # Κλείσιμο του server
        messagebox.showinfo("Επιτυχία", f"Email στάλθηκε επιτυχώς στον {to_address}")
    except Exception as e:
        messagebox.showerror("Σφάλμα", f"Σφάλμα κατά την αποστολή του email: {e}")

def search_and_display_results():
    date = entry.get()
    results = search_by_date(date)
    if results:
        result_window = tk.Toplevel(root)
        result_window.title("Αποτελέσματα Αναζήτησης")

        for result in results:
            customer_name = f"{result[1]} {result[2]}"
            appointment_datetime = result[4]

            result_label = tk.Label(result_window, text=f"Πελάτης: {customer_name}, Ημερομηνία: {appointment_datetime}")
            result_label.pack()

        send_button = tk.Button(result_window, text="Αποστολή Email Υπενθύμισης", command=lambda: send_reminder(results))
        send_button.pack()
    else:
        messagebox.showinfo("Καμία εγγραφή", "Δεν βρέθηκαν ραντεβού για την επιλεγμένη ημερομηνία.")

def send_reminder(results):
    for result in results:
        customer_email = result[3]
        customer_name = f"{result[1]} {result[2]}"
        appointment_datetime = result[4]

        subject = "Υπενθύμιση Ραντεβού"
        body = f"Αγαπητέ {customer_name},\n\nΥπενθύμιση για το ραντεβού σας στις {appointment_datetime}.\n\nΕυχαριστούμε!"

        send_email(
            to_address=customer_email,
            subject=subject,
            body=body
        )

root = tk.Tk()
root.title("Υπενθύμιση Ραντεβού")

search_label = tk.Label(root, text="Εισαγωγή Ημερομηνίας Αναζήτησης")
search_label.pack()

entry = tk.Entry(root)
entry.pack()

calendar = tkcalendar.Calendar(root, date_pattern="yyyy-mm-dd")

def show_calendar(event):
    calendar.pack()

entry.bind("<FocusIn>", show_calendar)

search_button = tk.Button(root, text="Αναζήτηση", command=search_and_display_results)
search_button.pack()

root.mainloop()
