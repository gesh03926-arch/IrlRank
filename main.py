from flask import Flask, request, render_template, redirect, url_for, session
from flask_bcrypt import Bcrypt
from extentions import db
from db_tables import Accounts
import json
import validation
import datetime
import os


app = Flask("main.py")


try:
    with open("database_config.json", "r") as config_file:
        config_dict = json.load(config_file)
except FileNotFoundError as e:
    print(e, "Could not find config.json, make sure it is included in the project")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+{drive}://{username}:{password}@{host}/{database}".format(
            drive = config_dict["drive"],
            username = config_dict["username"],
            password = config_dict["password"],
            host = config_dict["host"],
            database = config_dict["database"]
        )
    )
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#FIX THIS SECRET KEY, WHAT TO DO WITH IT?! its used in SESSION
app.secret_key = "wow"


db.init_app(app)
with app.app_context():
    db.create_all()

#Use this to hash passwords
bcrypt = Bcrypt(app)


@app.route("/")
def home():
    username = session.get("username")
    return render_template("home.html", username=username)

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        login_username = request.form['login_username']
        login_password = request.form['login_password']

        existing_account = Accounts.query.filter(
            Accounts.username == login_username
        ).first()

        if not existing_account:
            return render_template(
                template_name_or_list="login_page.html",
                username = "wrong",
                incorrect_username = login_username
            )

        account_password = existing_account.password
        password_match = bcrypt.check_password_hash(account_password, login_password)

        if not password_match:
            return render_template(
                template_name_or_list="login_page.html",
                password = "wrong",
                correct_username = login_username
            )
        session["username"] = login_username
        return redirect(location=url_for("home"))


    return render_template(
        template_name_or_list="login_page.html",

    )

@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method =="POST":
        account_name = request.form['signup_username']
        account_password = request.form['signup_password']
        account_email = request.form['signup_email']

        username_validation = validation.validate_user(account_name)
        if username_validation != "valid":
            error_message = username_validation
            return render_template(
                template_name_or_list="signup_page.html",
                username="invalid",
                error_message=error_message

            )

        existing_account = Accounts.query.filter(
            Accounts.username == account_name
        ).first()
        if existing_account:
            error_message = f"'{account_name}' is taken"
            return render_template(
                template_name_or_list="signup_page.html",
                username="invalid",
                error_message=error_message
            )

        password_validation = validation.validate_password(account_password)
        if password_validation != "valid":
            error_message = password_validation
            return render_template(
                template_name_or_list="signup_page.html",
                password="invalid",
                error_message=error_message,
                username = account_name,
                email = account_email
            )

        email_validation = validation.validate_email(account_email)
        if email_validation != "valid":
            error_message = email_validation
            return render_template(
                template_name_or_list="signup_page.html",
                email="invalid",
                error_message=error_message,
                username=account_name,
                password=account_password
            )

        hashed_password = bcrypt.generate_password_hash(account_password)
        account = Accounts(username = account_name, password = hashed_password, email = account_email)
        db.session.add(account)
        db.session.commit()
        return redirect(location=url_for("login"))

    return render_template(
        template_name_or_list="signup_page.html"
    )

#Executes the website when main.py is run, debug to see errors / HTTP requests,
if __name__ == "__main__":
    app.run(debug=True)

