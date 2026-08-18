from flask import Flask, request, render_template, redirect, url_for, session
from flask_bcrypt import Bcrypt
from extentions import db
from db_tables import Accounts
import json
import datetime
import os

#Creates the web app object
app = Flask("main.py")

#Gives the web app the necessary information to connect to the DB
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

#Connects web app to DB
db.init_app(app)

#Creates DB tables // dont really understand the use of app.context
with app.app_context():
    db.create_all()

#Creates bcrypt object, which is used to hash the passwords:
bcrypt = Bcrypt(app)

#Using app.route as a decorator. When the / page of the site gets accessed, it executes the login function
@app.route("/")
def home():
    username = session.get("username")
    return render_template("home.html", username=username)

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        login_username = request.form['login_username']
        login_password = request.form['login_password']

        #Check if account exists in DB based on username
        account_row = Accounts.query.filter(
            Accounts.username == login_username
        ).first()

        if not account_row:
            return render_template(
                template_name_or_list="login_page.html",
                username = "wrong",
                incorrect_username = login_username
            )

        account_password = account_row.password

        #Compares the hash of the password in the DB to the hash of the login password to see if they match
        if not bcrypt.check_password_hash(account_password, login_password):
            return render_template(
                template_name_or_list="login_page.html",
                password = "wrong",
                correct_username = login_username
            )

        session["username"] = login_username
        return redirect(location=url_for("home"))


    #When GET request:
    return render_template(
        template_name_or_list="login_page.html",

    )

@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method =="POST":
        account_name = request.form['signup_username']
        account_password = request.form['signup_password']
        hashed_password = bcrypt.generate_password_hash(account_password).decode("utf-8")

        account = Accounts(username = account_name, password = hashed_password)
        db.session.add(account)
        db.session.commit()
        return redirect(
            location=url_for("login")
        )
    return render_template(
        template_name_or_list="signup_page.html"
    )

#Executes the website when main.py is run, debug to see errors / HTTP requests,
if __name__ == "__main__":
    app.run(debug=True)

