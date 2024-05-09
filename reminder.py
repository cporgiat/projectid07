import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from search import search_by_date  # Εισαγωγή από το προηγούμενο αρχείο


# Στείλτε email υπενθύμισης
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
        print(f"Email στάλθηκε επιτυχώς στον {to_address}")
    except Exception as e:
        print(f"Σφάλμα κατά την αποστολή του email: {e}")


# Συνάρτηση υπενθύμισης για ραντεβού που πλησιάζουν
def send_appointment_reminder(date):
    # Αναζήτηση ραντεβού για μια συγκεκριμένη ημερομηνία
    results = search_by_date(date)

    if results:
        for result in results:
            customer_email = result[3]  # Λαμβάνουμε το email του πελάτη
            customer_name = f"{result[1]} {result[2]}"  # Ονοματεπώνυμο πελάτη
            appointment_datetime = result[4]  # Ημερομηνία και ώρα του ραντεβού

            # Δημιουργία του θέματος και του σώματος του email
            subject = "Υπενθύμιση Ραντεβού"
            body = f"Αγαπητέ {customer_name},\n\nΥπενθύμιση για το ραντεβού σας στις {appointment_datetime}.\n\nΕυχαριστούμε!"

            # Αποστολή του email υπενθύμισης
            send_email(
                to_address=customer_email,
                subject=subject,
                body=body
            )
    else:
        print("Δεν βρέθηκαν ραντεβού για την ημερομηνία αυτή.")


# Παράδειγμα χρήσης της συνάρτησης υπενθύμισης
if __name__ == "__main__":
    date = input("Εισάγετε την ημερομηνία για την οποία θέλετε να στείλετε υπενθυμίσεις (YYYY-MM-DD): ")
    send_appointment_reminder(date)
