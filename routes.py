from flask import Blueprint, request, jsonify
from app import db
from models import Customer
import bcrypt
import secrets

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/public', methods=['GET'])
def public():
    return 'Public'

@api_blueprint.route('/public/register', methods=['POST'])
def add_customer():
    data = request.get_json()

    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"message": "Missing required fields: email or password"}), 400
    
    email = data['email']
    password = data['password']

    existing_customer = Customer.query.filter_by(email=email).first()

    if existing_customer:
        return jsonify({"message": "Customer with this email already exists"}), 400
    
    new_customer = Customer(email=email, password=hash_password(password), personal_token=generate_personal_token())

    db.session.add(new_customer)
    db.session.commit()

    return jsonify({"message": f"Customer {email} registered successfully."}), 201

@api_blueprint.route('/public/personal_token', methods=['POST'])
def get_personal_token():
    data = request.get_json()

    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"message": "Missing required fields: email or password"}), 400
    
    email = data['email']
    password = data['password']

    existing_customer = Customer.query.filter_by(email=email).first()

    if not existing_customer:
        return jsonify({"message": "Customer not found."}), 404
    
    if not check_password(existing_customer.password, password):
        return jsonify({"message": "Invalid password."}), 400
    
    return jsonify({"token": existing_customer.personal_token}), 201

@api_blueprint.route('/public/send_token', methods=['POST'])
def send_personal_token():
    data = request.get_json()

    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"message": "Missing required fields: email or password"}), 400
    
    email = data['email']
    password = data['password']

    existing_customer = Customer.query.filter_by(email=email).first()

    if not existing_customer:
        return jsonify({"message": "Customer not found."}), 404
    
    if not check_password(existing_customer.password, password):
        return jsonify({"message": "Invalid password."}), 400
    
    return jsonify({"token": existing_customer.personal_token}), 201

@api_blueprint.route('/protected', methods=['GET'])
def protected():
    return 'Protected'

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()

    hash_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hash_password.decode('utf-8')

def generate_personal_token(length: int = 32) -> str:
    token = secrets.token_urlsafe(length)
    return token

def check_password(hash_password, password):
    return bcrypt.checkpw(password.encode('utf-8'), hash_password.encode('utf-8'))