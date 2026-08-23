import re


def validate_user(username : str):
    if len(username) < 3:
        return "Username must be at least 3 characters long"
    if len(username) >15:
        return "Username must be less than 15 characters long"
    pattern = re.compile(r'^[a-zA-Z0-9._]+$')
    if not re.match(pattern,username):
        return "Username contains invalid characters"
    if not re.match(r'[a-zA-Z]', username[0]):
        return "Username must start with a letter"

    return "valid"

def validate_password(password : str):
    if len(password) < 6:
        return "Password must contain at least 6 characters"
    if len(password) > 25:
        return "Password can not have more than 25 characters"
    return "valid"

def validate_email(email : str):
    if not re.match(r'^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$', email):
        return "Invalid email address"
    return "valid"
