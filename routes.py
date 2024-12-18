import os
from flask import Blueprint, request, jsonify
from app import db, mail
from models import Customer
from extensions import Message
import bcrypt
import secrets
import jwt
from flask_jwt_extended import jwt_required
import datetime

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

@api_blueprint.route('/public/signin', methods=['POST'])
def sign_in():
    data = request.get_json()

    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"message": "Missing required fields: email or password"}), 400
    
    email = data['email']
    password = data['password']

    existing_customer = Customer.query.filter_by(email=email).first()

    if existing_customer:
        return jsonify({"message": "Customer with this email already exists"}), 400
    
    if check_password(existing_customer.password, password):
        token = generate_token(existing_customer.id)
        return jsonify({'token': token}), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401

@api_blueprint.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return 'Protected'

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()

    hash_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hash_password.decode('utf-8')

def generate_personal_token(length: int = 32) -> str:
    token = secrets.token_urlsafe(length)
    return token

def generate_token(customer_id):
    payload = {
        'sub': customer_id,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, os.environ['secret_key'], algorithm='HS256')

    return token

def check_password(hash_password, password):
    return bcrypt.checkpw(password.encode('utf-8'), hash_password.encode('utf-8'))