# Python standard libraries
import json
import os
import sys

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
from jwt import ExpiredSignatureError
from sqlalchemy import update, delete, or_, and_
from oauthlib.oauth2 import WebApplicationClient
import requests
from fuzzywuzzy import process, fuzz
from random_username.generate import generate_username
import mailtrap as mt
import jwt
import os
from datetime import datetime, timedelta, timezone

# Internal imports
from extentions import db
from db_tables import Users, MarkedDates, ProfileRequests, Friendships
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

#ENV variables
app.secret_key = os.getenv("APP_SECRET_KEY")
mailtrap_api = os.getenv("MAILTRAP_API")

# User session management setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.anonymous_user = AnonymousUser

#Use this to hash passwords
bcrypt = Bcrypt(app)

# with app.app_context():
#     print("start")
#     rand_usernames = generate_username(10000)
#     for i in range(1000):
#         rand_user = Users(
#             username=rand_usernames[i],
#             password=bcrypt.generate_password_hash("12345678"),
#             email=rand_usernames[i] + '@gmail.com',
#         )
#         db.session.add(rand_user)
#         print("added ", i)
#     db.session.commit()
#     print("end")

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(Users).get(user_id)

@app.route('/users/search', methods=["GET","POST"])
def users_search():

    searched = request.args.get("searched")
    if request.method == "POST":
        redirect_url = nav_menu_submits('users_search', searched=searched)
        if redirect_url:
            return redirect(redirect_url)

        request_user_id = int(request.form.get("request_button"))
        profile_request = ProfileRequests(
            sender_user_id = current_user.id,
            receiver_user_id = request_user_id
        )
        db.session.add(profile_request)
        db.session.commit()
        return redirect(url_for('users_search', searched=searched))

    receiving_users_ids= []
    for user_request in current_user.sent_requests:
        receiving_users_ids.append(user_request.receiver_user_id)

    similar_users = []
    for user in Users.query.all():
        name = user.username
        if name == current_user.username:
            continue
        similarity = fuzz.WRatio(searched, name)
        if similarity>80:
            user.ratio = similarity
            user.request = "not sent"
            if user.id in receiving_users_ids:
                user.request = "sent"
            similar_users.append(user)

    matches = {}
    matches_sections=0
    for i in range(len(similar_users)):
        user = similar_users[i]
        user_section = str( int(i/10)+1 )
        if not matches.get(user_section):
            matches[user_section] = [user]
            matches_sections = int(user_section)
            continue
        matches.get(user_section).append(user)


    current_user.searched = searched
    section = "1"
    if request.args.get("section"):
        section = request.args.get("section")

    return render_template(
        template_name_or_list='user_search.html',
        matches = matches,
        matches_sections = matches_sections,
        section = section
    )
@app.route('/users/info', methods = ["GET", "POST"])
def users_info():

    user_name = request.args.get("user")

    if request.method == "POST":
        redirect_url = nav_menu_submits('users_info', user = user_name)
        if redirect_url:
            return redirect(redirect_url)

    user = Users.query.filter(
        Users.username == user_name
    ).first()

    mark_dict = get_dates_from_db(user.id)
    return render_template(
        template_name_or_list='users_info.html',
        mark_dict = json.dumps(mark_dict),
        hours_worked = user.hours_worked,
        user_name = user.username,
        markable_bool = "false",
        work_name = user.work
    )

@app.route("/", methods = ["GET", "POST"])
def home():

    if current_user.is_anonymous:
        if request.method == "POST":
            work_name = request.form.get("work_name")
            session['work'] = work_name
            return redirect(url_for('signup'))
        return render_template(
            template_name_or_list="landing_page.html"
        )

    if request.method == "POST":
        redirect_url = nav_menu_submits('home')
        if redirect_url:
            return redirect(redirect_url)

        hours_input = float(request.form.get("hours_worked"))
        if hours_input<0:
            remove_dict_json = request.form.get("remove_dict")
            remove_dict = json.loads(remove_dict_json)
            print(remove_dict)
            for month_year, position_date_arr in remove_dict.items():
                delete_row = (delete(MarkedDates)
                    .where(MarkedDates.month_and_year == month_year)
                    .where(MarkedDates.position == position_date_arr[0])
                    .where(MarkedDates.date == position_date_arr[1])
                    .where(MarkedDates.user_id == current_user.id)
                )
                db.session.execute(delete_row)
            remove_hours = update(Users).where(Users.id == current_user.id).values(hours_worked = current_user.hours_worked - (-hours_input))
            db.session.execute(remove_hours)
            db.session.commit()
            return redirect((url_for('home')))

        mark_dict_from_js = json.loads(request.form.get("mark_dict"))
        add_dates_to_db(mark_dict_from_js)
        add_hours = update(Users).where(Users.id == current_user.id).values(hours_worked=current_user.hours_worked + hours_input)
        db.session.execute(add_hours)
        db.session.commit()
        session["month_year"] = request.form.get("month_year")
        return redirect(url_for('home'))

    mark_dict = get_dates_from_db(current_user.id)
    if not session.__contains__("month_year"):
        session["month_year"] = ""

    return render_template(
        template_name_or_list="home.html",
        mark_dict = json.dumps(mark_dict),
        month_year = session["month_year"],
        hours_worked = current_user.hours_worked,
        markable_bool = "true",
        work_name = current_user.work
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
    session['work'] = None
    session["month_year"] = ""
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

    return redirect(request_uri)
@app.route("/login/google/callback")
def login_google_callback():
    google_code = request.args.get("code")
    token_endpoint = google_provider_config["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url = request.base_url,
        code=google_code

    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(oauth_config["client_id"], oauth_config["client_secret"])
    )
    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_config["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    already_registered_user =Users.query.filter(
        Users.email == users_email
    ).first()
    if already_registered_user:
        login_user(already_registered_user, remember=True)
    else:
        user = Users(
            username = users_name,
            email = users_email,
            work = session.get('work'),
            pfp_path = picture
        )
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)

    return redirect(url_for("home"))


@app.route("/signup", methods = ["GET", "POST"])
def signup():
    current_user.work = session.get("work")
    if request.method =="POST":
        signup_username = request.form['signup_username']
        signup_password = request.form['signup_password']
        signup_email = request.form['signup_email']
        signup_workname = ""

        username_check = password_check = email_check = workname_check = "valid"
        error_message_u = error_message_p = error_message_e = error_message_w = None

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

        if request.form.get("signup_workname"):
            signup_workname = request.form.get("signup_workname")
            workname_validation = validation.validate_workname(signup_workname)
            if workname_validation != "valid":
                error_message_w = workname_validation
                workname_check = "invalid"
            else:
                current_user.work = request.form.get("signup_workname")

        if username_check == "invalid" or password_check == "invalid" or email_check == "invalid" or workname_check == "invalid":
            incorrect_signup_values = {
                "username_check": username_check,
                "password_check": password_check,
                "email_check": email_check,
                "workname_check":workname_check,
                "signup_username": signup_username,
                "signup_password": signup_password,
                "signup_email": signup_email,
                "signup_workname": signup_workname,
                "error_message_u": error_message_u,
                "error_message_p": error_message_p,
                "error_message_e": error_message_e,
                "error_message_w": error_message_w
            }
            return render_template(
                template_name_or_list="signup_page.html",
                **incorrect_signup_values
            )

        hashed_password = bcrypt.generate_password_hash(signup_password)
        user = Users(
            username = signup_username,
            password = hashed_password,
            email = signup_email,
            work = current_user.work
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(location=url_for("home"))


    return render_template(
        template_name_or_list="signup_page.html"
    )

@app.route('/recovery', methods = ["GET", "POST"])
def recovery():
    if request.method == "POST":
        input_email = request.form.get("recovery_email")
        email_exists = Users.query.filter(
            Users.email == input_email
        ).first()
        current_user.entered_email = input_email

        if not email_exists:
            return render_template(
                template_name_or_list='recovery.html',
                email="invalid",
                entered_email = input_email
            )

        token = jwt.encode(
            {'email':input_email, "exp": datetime.now(tz = timezone.utc) + timedelta(minutes=1)},
            key=app.secret_key,
            algorithm="HS256",
        )
        recovery_link = f"https://127.0.0.1:5000/recovery/password?info={token}"
        email = mt.Mail(
            sender = mt.Address("hello@demomailtrap.co", name="Test"),
            to = [mt.Address("gesh03926@gmail.com")],
            subject = "Worktracker password recovery",
            text = f"Click the link below to access the password recovery \n {recovery_link} \n You have around 5 minutes before the link becomes invalid",
            category= "Integration Test"
        )
        client = mt.MailtrapClient(token = mailtrap_api)
        # response = client.send(email) EXPIRED TOKENS FOR EMAIL FROM THEIR DOMAIN
        print(recovery_link)

        return render_template(
            template_name_or_list='recovery.html',
            email_sent =True,
            entered_email = input_email
        )

    return render_template(
        template_name_or_list='recovery.html',
        email = "ok"
    )

@app.route('/recovery/password', methods = ["GET", "POST"])
def change_password():
    token = request.args.get("info")
    try:
        token_info = jwt.decode(token, key=app.secret_key, algorithms="HS256", leeway=30)
    except ExpiredSignatureError:
        return redirect(url_for('token_expired'))

    if request.method =="POST":
        new_pass = request.form.get("new_password")
        password_validation = validation.validate_password(new_pass)
        if password_validation != "valid":
            return render_template(
                template_name_or_list='change_password.html',
                password_check = "invalid",
                error_message_p = password_validation,
                entered_password = new_pass

            )

        new_pass_confirm = request.form.get("new_password_confirm")
        if new_pass != new_pass_confirm:
            return render_template(
                template_name_or_list='change_password.html',
                password_match = False,
                entered_password = new_pass,
                entered_password2 = new_pass_confirm
            )

        user_email = token_info.get("email")
        hashed_pass = bcrypt.generate_password_hash(new_pass)
        change_pass = update(Users).where(Users.email == user_email).values(password = hashed_pass)
        db.session.execute(change_pass)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template(
        template_name_or_list='change_password.html'
    )

@app.route('/recovery/expired')
def token_expired():
    return render_template(
        template_name_or_list='token_expired.html'
    )
def nav_menu_submits(current_url:str, **values):
    if request.form.get("searched_user"):
        searched = request.form.get("searched_user")
        return url_for('users_search', searched=searched)
    if request.form.get("private_button"):
        button_change = request.form.get("private_button")
        status = True
        if button_change == "false":
            status = False
        alter_private = update(Users).where(Users.id == current_user.id).values(is_private=status)
        db.session.execute(alter_private)
        db.session.commit()
        return url_for(current_url, **values)
    if request.form.get("accept_req_button"):
        sender_id = request.form.get("accept_req_button")
        friendship = Friendships(
            start_user_id=sender_id,
            accept_user_id=current_user.id
        )
        db.session.add(friendship)
        delete_request = (delete(ProfileRequests)
                          .where(ProfileRequests.sender_user_id == int(sender_id))
                          .where(ProfileRequests.receiver_user_id == current_user.id)
        )
        db.session.execute(delete_request)
        db.session.commit()
        return url_for(current_url, **values)
    if request.form.get("reject_req_button"):
        sender_id = request.form.get("reject_req_button")
        delete_request = (delete(ProfileRequests)
                          .where(ProfileRequests.sender_user_id == int(sender_id))
                          .where(ProfileRequests.receiver_user_id == current_user.id)
        )
        db.session.execute(delete_request)
        db.session.commit()
        return url_for(current_url, **values)
    if request.form.get("removed_friend_id"):
        removed_friend_id = request.form.get("removed_friend_id")
        remove_friend = (delete(Friendships).where(
                    or_(
                        and_(
                            Friendships.accept_user_id == current_user.id, Friendships.start_user_id == removed_friend_id
                            ),
                and_(
                            Friendships.accept_user_id == removed_friend_id, Friendships.start_user_id == current_user.id
                            )
                        )
                )
        )

        db.session.execute(remove_friend)
        db.session.commit()
        return url_for(current_url, **values)


    if request.form.get("new_pfp"):
        new_pfp = request.form.get("new_pfp")
        update_user_pfp = (update(Users)
                           .where(Users.id == current_user.id)
                           .values(pfp_path = f"../static/website_images/{new_pfp}")
        )
        db.session.execute(update_user_pfp)
        db.session.commit()
        return url_for(current_url, **values)

    return None

def add_dates_to_db(mark_dict: dict):
    for month_year in mark_dict:
        marked_dates = mark_dict[month_year]
        left_dates = marked_dates["left"][0]
        left_hours = marked_dates["left"][1]
        for i in range(len(left_dates)):
            print(len(left_dates))
            exists = MarkedDates.query.filter(
                MarkedDates.month_and_year == month_year,
                MarkedDates.date == left_dates[i],
                MarkedDates.position == "left",
                MarkedDates.user_id == current_user.id
            ).first()
            if not exists:
                new_marked_date = MarkedDates(
                    month_and_year=month_year,
                    date=left_dates[i],
                    position="left",
                    hours=left_hours[i],
                    user_id=current_user.id
                )
                db.session.add(new_marked_date)
        current_dates = marked_dates["current"][0]
        current_hours = marked_dates["current"][1]
        for i in range(len(current_dates)):
            exists = MarkedDates.query.filter(
                MarkedDates.month_and_year == month_year,
                MarkedDates.date == current_dates[i],
                MarkedDates.position == "current",
                MarkedDates.user_id == current_user.id
            ).first()
            if not exists:
                new_marked_date = MarkedDates(
                    month_and_year=month_year,
                    date=current_dates[i],
                    position="current",
                    hours=current_hours[i],
                    user_id=current_user.id
                )
                db.session.add(new_marked_date)
        right_dates = marked_dates["right"][0]
        right_hours = marked_dates["right"][1]
        for i in range(len(right_dates)):
            exists = MarkedDates.query.filter(
                MarkedDates.month_and_year == month_year,
                MarkedDates.date == right_dates[i],
                MarkedDates.position == "right",
                MarkedDates.user_id == current_user.id
            ).first()
            if not exists:
                new_marked_date = MarkedDates(
                    month_and_year=month_year,
                    date=right_dates[i],
                    position="right",
                    hours=right_hours[i],
                    user_id=current_user.id
                )
                db.session.add(new_marked_date)
    db.session.commit()

def get_dates_from_db(user_id : int) -> dict:
    mark_dict = {}
    for row in (MarkedDates.query.all()):
        if row.user_id != user_id:
            continue
        if not mark_dict.__contains__(row.month_and_year):
            inner_dict = {"left": [[], []], "current": [[], []], "right": [[], []]}
            position_dates_hours = inner_dict.get(row.position)
            dates = position_dates_hours[0]
            dates.append(row.date)
            hours = position_dates_hours[1]
            hours.append(row.hours)
            mark_dict[row.month_and_year] = inner_dict
        else:
            inner_dict = mark_dict.get(row.month_and_year)
            position_dates_hours = inner_dict.get(row.position)
            dates = position_dates_hours[0]
            dates.append(row.date)
            hours = position_dates_hours[1]
            hours.append(row.hours)
    return mark_dict


# def remove_dates_from_db(remove_dict : dict):

#Executes the website when main.py is run, debug to see errors / HTTP requests,
if __name__ == "__main__":
    app.run(debug=True, ssl_context = "adhoc") # ssl_context is shortcut to get HTTPS protocol, not good longterm maybe



