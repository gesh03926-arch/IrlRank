#DB object needed in main.py and db_tables.py
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

#Project root filepath
import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
