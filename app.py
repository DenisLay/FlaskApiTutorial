import os
from flask import Flask
from extensions import db, mail
from routes import api_blueprint

def create_app(name, debug):
    app = Flask(name)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["db_uri"]
    app.config['DEBUG'] = debug
    mail.init_app(app)
    db.init_app(app)

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = os.environ["email_link"]
    app.config['MAIL_PASSWORD'] = os.environ["email_password"]
    app.config['MAIL_DEFAULT_SENDER'] = os.environ["email_link"]

    app.register_blueprint(api_blueprint)

    with app.app_context():
        db.create_all()

    return app