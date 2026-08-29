from extentions import db
from sqlalchemy import Integer, String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_login import UserMixin

class Users(db.Model, UserMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(250))
    password: Mapped[str] = mapped_column(String(250), nullable=True)
    email: Mapped[str] = mapped_column(String(250))
    pfp_path: Mapped[String] = mapped_column(String(500), nullable=True)

    #Non-DB attributes of users object, simplify work with current_user
    account_action = "logout"
    account_action_text = "Sign out"





