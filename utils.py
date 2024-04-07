import re

def validate_input_only_letters(ap_text):
    if(re.match(r'^[A-Za-zΑ-Ωα-ω]+$', ap_text)):
        return True
    else:
        return False

def validate_input_only_numbers(ap_text):
    if(re.match(r'^[0-9]+$', ap_text)):
        return True
    else:
        return False

def validate_input_email(ap_text):
    if(re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', ap_text)):
        return True
    else:
        return False

def get_name(ap_text):

    while(True):
        ap_input=input(ap_text)
        if(validate_input_only_letters(ap_input)):
            break
        else:
            print("Παρακαλω χρησιμοποιηστε μονο Ελληνικους η Λατινικους χαρακτηρες χωρις κενα. Δοκιμαστε παλι.")

    return ap_input

def get_number(ap_text):

    while(True):
        ap_input=input(ap_text)
        if(validate_input_only_numbers(ap_input)):
            break
        else:
            print("Παρακαλω χρησιμοποιηστε μονο αριθμους χωρις κενα. Δοκιμαστε παλι.")

    return ap_input

def get_email(ap_text):

    while(True):
        ap_input=input(ap_text)
        if(validate_input_email(ap_input)):
            break
        else:
            print("Μη σωστο email. Παρακαλω χρησιμοποιηστε μονο πεζους Λατινικους χαρακτηρες χωρις κενα. Δοκιμαστε παλι.")

    return ap_input
