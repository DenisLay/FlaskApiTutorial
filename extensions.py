from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, create_engine, text, MetaData, Table
from flask_mail import Mail, Message
db = SQLAlchemy()
mail = Mail()