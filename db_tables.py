from extentions import db
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import relationship
from flask_login import UserMixin

class Users(db.Model, UserMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(250))
    password: Mapped[str] = mapped_column(String(250), nullable=True)
    email: Mapped[str] = mapped_column(String(250))
    work: Mapped[str] = mapped_column(String(40), default = "No work name")
    hours_worked: Mapped[int] = mapped_column(default=0)
    is_private: Mapped[bool] = mapped_column(default=False)
    pfp_path: Mapped[str] = mapped_column(String(500), default = "../static/website_images/anon_pfp.png")

    sent_requests =db.relationship("ProfileRequests", foreign_keys = "ProfileRequests.sender_user_id")
    receiving_requests = db.relationship("ProfileRequests", foreign_keys ="ProfileRequests.receiver_user_id")
    started_friendships = db.relationship("Friendships", foreign_keys = "Friendships.start_user_id")
    accepted_friendships = db.relationship("Friendships", foreign_keys = "Friendships.accept_user_id")


    #Non-DB attributes of users object, simplify work with current_user
    account_action = "logout"
    account_action_text = "Sign out"

    #Important current_user functions:
    @property
    def request_senders(self):
        senders=[]
        for receiving_request in self.receiving_requests:
            senders.append(db.session.get(Users, receiving_request.sender_user_id))
        return senders

    @property
    def friends(self):
        friends = []
        for started in self.started_friendships:
            friends.append(db.session.get(Users, started.accept_user_id))
        for accepted in self.accepted_friendships:
            friends.append(db.session.get(Users,accepted.start_user_id))
        return friends


class MarkedDates(db.Model):
    __tablename__= "marked_dates"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    month_and_year: Mapped[str] = mapped_column(String(10))
    date: Mapped[str] = mapped_column(String(5))
    position: Mapped[str] = mapped_column(String(10))
    hours: Mapped[int] = mapped_column(default=0)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)

class ProfileRequests(db.Model):
    __tablename__ = "requests"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sender_user_id: Mapped[int] = mapped_column(ForeignKey('users.id'),index=True)
    receiver_user_id: Mapped[int] = mapped_column(ForeignKey('users.id'),index=True)
    status: Mapped[str] = mapped_column(String(30), default = "pending")

class Friendships(db.Model):
    __tablename__ = "friendships"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    start_user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    accept_user_id : Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
