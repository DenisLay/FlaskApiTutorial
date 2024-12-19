import os
from flask import Flask
from extensions import db
from routes import api_blueprint
from flask_jwt_extended import JWTManager

def create_app(name, debug):
    app = Flask(name)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['db_uri']
    app.config['SECRET_KEY'] = os.environ['secret_key']
    app.config['DEBUG'] = debug
    mail.init_app(app)
    db.init_app(app)
    jwt = JWTManager(app)

    app.register_blueprint(api_blueprint)

    with app.app_context():
        db.create_all()

    return app