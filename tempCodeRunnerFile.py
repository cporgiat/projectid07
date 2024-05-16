n.cursor()
        sql = """
            SELECT app.id, cust.firstname, cust.lastname, app.datetime, app.duration
            FROM appointments app
            JOIN customers cust ON app.customerid = cust.id
            WHERE DATE(app.datetime) = ?
        """
        results = cursor.execute(sql, (date,)).fetchall()
    return results


# Συνάρτηση αναζήτησης με βάση το email πελάτη
def search_by_customer_email(email):
    with get_connection() as conn: