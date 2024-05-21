import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from search import search_by_date  # Εισαγωγή από το προηγούμενο αρχείο
from tkinter import messagebox


# Στείλτε email υπενθύμισης
def send_email(to_address, subject, body, from_address='ypenthimisirantevou@mail.com', smtp_server='smtp-relay.brevo.com',
               smtp_port=587, smtp_user='750db5001@smtp-brevo.com', smtp_pass='YHSpbzaq208AmCNB'):
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


# Συνάρτηση υπενθύμισης για ραντεβού που πλησιάζουν
def send_reminder(results):
    for result in results:
        customer_email = result[5]
        customer_name = f"{result[1]} {result[2]}"
        appointment_datetime = result[3]

        subject = "Υπενθύμιση Ραντεβού"
        body = f"Αγαπητέ {customer_name},\n\nΥπενθύμιση για το ραντεβού σας στις {appointment_datetime}.\n\nΕυχαριστούμε!"

        send_email(
            to_address=customer_email,
            subject=subject,
            body=body
        )


