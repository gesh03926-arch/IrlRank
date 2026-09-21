import re
from db_tables import Users

def validate_username(username : str) -> str:
    if len(username) < 3:
        return "Username must be at least 3 characters long"
    if len(username) >15:
        return "Username must be less than 15 characters long"
    pattern = re.compile(r'^[a-zA-Z0-9._]+$')
    if not re.match(pattern,username):
        return "Username contains invalid characters"
    if not re.match(r'[a-zA-Z]', username[0]):
        return "Username must start with a letter"

    same_username_account = Users.query.filter(
        Users.username == username
    ).first()
    if same_username_account:
        return f"{username} is taken"

    return "valid"

def validate_password(password : str) -> str:
    if len(password) < 6:
        return "Password must contain at least 6 characters"
    if len(password) > 25:
        return "Password can not have more than 25 characters"
    return "valid"

def validate_email(email : str) -> str:
    if not re.match(r'^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$', email):
        return "Invalid email address"
    same_email_account = Users.query.filter(
        Users.email == email
    ).first()
    if same_email_account:
        return "Email address is already registered"
    return "valid"


def validate_workname(workname : str) -> str:
    if len(workname) <2:
        return "Workname must be at least 2 characters long!"
    if len(workname) >=15:
        return "Workname is too long - shorten it!"
    return "valid"