from flask import Flask
from extensions import db, create_engine, text
from routes import api_blueprint

def create_app(name, db_uri, debug):
    app = Flask(name)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['DEBUG'] = debug
    app.register_blueprint(api_blueprint)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app