import os
from flask import Flask
from extensions import db, mail
from routes import api_blueprint

def create_app(name, debug):
    app = Flask(name)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['db_uri']
    app.config['SECRET_KEY'] = os.environ['secret_key']
    app.config['DEBUG'] = debug
    mail.init_app(app)
    db.init_app(app)

    app.register_blueprint(api_blueprint)

    with app.app_context():
        db.create_all()

    return app