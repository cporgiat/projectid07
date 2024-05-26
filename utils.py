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
















