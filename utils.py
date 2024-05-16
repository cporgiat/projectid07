import re
from datetime import datetime


def validate_input_only_letters(ap_text):
    """ This function checks input against a regex expression to validate
    if the string is only upper/lower case greek or latin characters
    and returns true"""
    if (re.match(r'^[A-Za-zΑ-Ωα-ω]+$', ap_text)):
        return True
    else:
        return False


def validate_input_only_numbers(ap_text):
    """ This function checks input against a regex expression to validate
    if the string is only number characters and returns true"""
    if (re.match(r'^[0-9]+$', ap_text)):
        return True
    else:
        return False


def validate_input_email(ap_text):
    """ This function checks input against a regex expression to validate
    if the string is in format of <string>@<string>.<string> and returns true"""
    if (re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', ap_text)):
        return True
    else:
        return False


def validate_input_datetime(ap_text):
    """ This function checks input to validate if the string
    is a valid date in the format of <year>-<month>-<day> <24hours>:<minutes> and returns true"""
    try:
        datetime.strptime(ap_text, "%Y-%m-%d %H:%M")
        return True
    except ValueError:
        return False


def validate_future_datetime(ap_text):
    """ This function checks input to validate if the string
    is a valid date in the format of <year>-<month>-<day> <24hours>:<minutes>
    and is the future and returns true"""
    try:
        checkdate = datetime.strptime(ap_text, "%Y-%m-%d %H:%M")
        if (checkdate > datetime.now()):
            return True
        else:
            return False
    except ValueError:
        return False


def get_name(ap_text):
    while (True):
        ap_input = input(ap_text)
        if (validate_input_only_letters(ap_input)):
            break
        else:
            print("Παρακαλω χρησιμοποιηστε μονο Ελληνικους η Λατινικους χαρακτηρες χωρις κενα. Δοκιμαστε παλι.")

    return ap_input


def get_number(ap_text):
    while (True):
        ap_input = input(ap_text)
        if (validate_input_only_numbers(ap_input)):
            break
        else:
            print("Παρακαλω χρησιμοποιηστε μονο αριθμους χωρις κενα. Δοκιμαστε παλι.")

    return ap_input


def get_phone(ap_text):
    while (True):
        ap_input = input(ap_text)
        if (validate_input_only_numbers(ap_input) and len(ap_input)==9):
            break
        else:
            print("Λαθος μορφη τηλεφωνου. Επιτρεπονται μονο 9αψηφιοι θετικοι αριθμοι χωρις κενα. Δοκιμαστε παλι.")

    return ap_input

def get_email(ap_text):
    while (True):
        ap_input = input(ap_text)
        if (validate_input_email(ap_input)):
            break
        else:
            print(
                "Λαθος μορφη email. Επιτρεπονται μονο πεζοι Λατινικοι χαρακτηρες, @ και . χωρις κενα. Δοκιμαστε παλι.")

    return ap_input


def get_datetime(ap_text):
    while (True):
        ap_input = input(ap_text)
        if (validate_input_datetime(ap_input)):
            break
        else:
            print("Λαθος μορφη ημερομηνιας. Παρακαλω εισαγετε ημερομηνια στην μορφη ΥΥΥΥ-ΜΜ-DD HH:MI. Δοκιμαστε παλι.")

    return ap_input


def get_duration(ap_text):
    while (True):
        ap_input = input(ap_text)
        if ap_input == "":
            ap_input = '30'

        if (validate_input_only_numbers(ap_input)):
            break
        else:
            print("Παρακαλω χρησιμοποιηστε μονο αριθμους χωρις κενα. Δοκιμαστε παλι.")

    return ap_input