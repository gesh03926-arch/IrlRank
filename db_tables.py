from extentions import db
from sqlalchemy import Integer, String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Users(db.Model):
    id: Mapped[int] = mapped_column(primary_key =True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30))
    age: Mapped[str] = mapped_column(String(3))
    irl_rank: Mapped[str] = mapped_column(String(5), default="")



class Accounts(db.Model):
    __tablename__ = "accounts"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(25))
    password: Mapped[str] = mapped_column(String(150))