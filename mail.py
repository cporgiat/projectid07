import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Σύνδεση με τη βάση δεδομένων
conn = sqlite3.connect('appointments.db')
cursor = conn.cursor()


# Λειτουργία αναζήτησης με βάση το όνομα του πελάτη
def search_appointments_by_customer_name(name):
    sql = """
        SELECT app.id, cust.firstname, cust.lastname, cust.email, app.datetime, app.duration 
        FROM appointments app
        JOIN customers cust ON app.customerid = cust.id
        WHERE cust.firstname LIKE ? OR cust.lastname LIKE ?
    """
    results = cursor.execute(sql, (f"%{name}%", f"%{name}%",)).fetchall()
    return results


# Λειτουργία αποστολής email
def send_email(recipient_email, subject, body):
    # Αντικατάστησε τα παρακάτω με τις πληροφορίες SMTP σου
    smtp_server = "smtp.example.com"  # Αντικατάστησε με τον SMTP διακομιστή σου
    smtp_port = 587  # Ή οποιαδήποτε άλλη πόρτα χρησιμοποιεί ο διακομιστής σου
    smtp_user = "your_email@example.com"  # Το email σου
    smtp_pass = "your_password"  # Ο κωδικός πρόσβασης σου

    # Δημιουργία μηνύματος email
    message = MIMEMultipart()
    message["From"] = smtp_user
    message["To"] = recipient_email
    message["Subject"] = subject

    # Προσθήκη του σώματος του μηνύματος
    message.attach(MIMEText(body, "plain"))

    # Αποστολή του email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Χρήση κρυπτογράφησης TLS
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, recipient_email, message.as_string())


# Αναζήτηση ραντεβού με βάση το όνομα του πελάτη
customer_name = input("Εισάγετε το όνομα του πελάτη για αναζήτηση ραντεβού: ")
results = search_appointments_by_customer_name(customer_name)

# Αν υπάρχουν αποτελέσματα, αποστολή email υπενθύμισης
if results:
    for row in results:
        appointment_id = row[0]
        customer_firstname = row[1]
        customer_lastname = row[2]
        customer_email = row[3]
        appointment_datetime = row[4]

        # Δημιουργία μηνύματος υπενθύμισης
        subject = f"Υπενθύμιση για το ραντεβού σας"
        body = f"Αγαπητέ {customer_firstname} {customer_lastname},\n\n" + \
               f"Θα θέλαμε να σας υπενθυμίσουμε ότι έχετε ραντεβού στις {appointment_datetime}.\n\n" + \
               "Ευχαριστούμε!"

        # Αποστολή email υπενθύμισης
        send_email(customer_email, subject, body)

    print("Υπενθυμίσεις εστάλησαν.")
else:
    print("Δεν βρέθηκαν ραντεβού για αυτό το όνομα.")
