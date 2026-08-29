# Python standard libraries
import json
import os

# Third-party libraries
from flask import Flask, request, render_template, redirect, url_for, session
from flask_bcrypt import Bcrypt
from flask_login import(
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
    UserMixin,
    AnonymousUserMixin
)
import oauthlib
from oauthlib.oauth2 import WebApplicationClient
import requests

# Internal imports
from extentions import db
from db_tables import Users
import validation
import configs
from anonymous_user_info import AnonymousUser


#Configuration
db_info = configs.get_db_config_info()
oauth_config = configs.get_oauth_config_info()
GOOGLE_CLIENT_ID = oauth_config['client_id']
google_provider_config = configs.get_google_provider_config()
#Oauth2 client setup:
client = WebApplicationClient(GOOGLE_CLIENT_ID)


app = Flask("main.py")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+{drive}://{username}:{password}@{host}/{database}".format(
            drive = db_info["drive"],
            username = db_info["username"],
            password = db_info["password"],
            host = db_info["host"],
            database = db_info["database"]
        )
    )
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

app.secret_key = os.getenv("APP_SECRET_KEY")

# User session management setup
# https://flask-login.readthedocs.io/en/latest // Got this from a tutorial, figure it out
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.anonymous_user = AnonymousUser

#Use this to hash passwords
bcrypt = Bcrypt(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(Users).get(user_id)

@app.route("/")
def home():
    return render_template(
        template_name_or_list="home.html",
    )

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        login_username = request.form['login_username']
        login_password = request.form['login_password']

        existing_user = Users.query.filter(
            Users.username == login_username
        ).first()

        if not existing_user:
            return render_template(
                template_name_or_list="login_page.html",
                username = "wrong",
                incorrect_username = login_username
            )

        account_password = existing_user.password
        password_match = bcrypt.check_password_hash(account_password, login_password)

        if not password_match:
            return render_template(
                template_name_or_list="login_page.html",
                password = "wrong",
                correct_username = login_username
            )
        remember = False
        checked_remember_box = request.form.getlist('remember_box')
        if checked_remember_box:
            remember = True


        login_user(existing_user, remember=remember)

        return redirect(url_for("home"))

    return render_template(
        template_name_or_list="login_page.html",

    )

@app.route("/redirect/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/login/google")
def login_google():
    # Find out what URL to hit for Google login
    authorization_endpoint = google_provider_config["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile info from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri = request.base_url + "/callback",
        scope = ["openid", "email", "profile"]
    )
    print(request_uri, " this is request url")
    return redirect(request_uri)
@app.route("/login/google/callback")
def login_google_callback():
    # Get authorization code Google sent back to you
    google_code = request.args.get("code")
    # Find out what URL to hit to get tokens that allow you to ask for things on behalf of a user
    token_endpoint = google_provider_config["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url = request.base_url,
        #code already gets parsed from request.base_url, but probably doesnt hurt to include it twice?
        code=google_code

    )

    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(oauth_config["client_id"], oauth_config["client_secret"])
    )

    #### STIGNAH DO TUK - trqbva da razbera zashto post requesta se nujda ot headers, data i auth
    ### Trqbva da razbera zashto kato parsenem responsa ne go zapazvame kato variable
    # i da se produlji nadolu kak se sluchva

    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_config["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    #Check if user is already registered in DB
    already_registered_user =Users.query.filter(
        Users.email == users_email
    ).first()
    if already_registered_user:
        login_user(already_registered_user, remember=True)
    else:
        user = Users(username = users_name, email = users_email, pfp_path = picture)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)


    return redirect(url_for("home"))


@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method =="POST":
        signup_username = request.form['signup_username']
        signup_password = request.form['signup_password']
        signup_email = request.form['signup_email']
        username_check = password_check = email_check = "valid"
        error_message_u = error_message_p = error_message_e = None

        username_validation = validation.validate_username(signup_username)
        if username_validation != "valid":
            error_message_u = username_validation
            username_check = "invalid"

        password_validation = validation.validate_password(signup_password)
        if password_validation != "valid":
            error_message_p = password_validation
            password_check = "invalid"

        email_validation = validation.validate_email(signup_email)
        if email_validation != "valid":
            error_message_e = email_validation
            email_check = "invalid"

        if username_check == "invalid" or password_check == "invalid" or email_check == "invalid":
            incorrect_signup_values = {
                "username_check": username_check,
                "password_check": password_check,
                "email_check": email_check,
                "signup_username": signup_username,
                "signup_password": signup_password,
                "signup_email": signup_email,
                "error_message_u": error_message_u,
                "error_message_p": error_message_p,
                "error_message_e": error_message_e
            }
            return render_template(
                template_name_or_list="signup_page.html",
                **incorrect_signup_values
            )

        hashed_password = bcrypt.generate_password_hash(signup_password)
        user = Users(username = signup_username, password = hashed_password, email = signup_email ,pfp_path = "../static/anon_pfp.png")
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(location=url_for("home"))

    return render_template(
        template_name_or_list="signup_page.html"
    )


#Executes the website when main.py is run, debug to see errors / HTTP requests,
if __name__ == "__main__":
    app.run(debug=True, ssl_context="adhoc") # ssl_context is shortcut to get HTTPS protocol, not good longterm maybe

