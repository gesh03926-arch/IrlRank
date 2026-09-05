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
    work: Mapped[str] = mapped_column(String(40))
    hours_worked: Mapped[int] = mapped_column(default=0)
    pfp_path: Mapped[str] = mapped_column(String(500), nullable=True)

    #Non-DB attributes of users object, simplify work with current_user
    account_action = "logout"
    account_action_text = "Sign out"

class MarkedDates(db.Model):
    __tablename__= "marked_dates"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    month_and_year: Mapped[str] = mapped_column(String(10))
    date: Mapped[str] = mapped_column(String(5))
    position: Mapped[str] = mapped_column(String(10))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

