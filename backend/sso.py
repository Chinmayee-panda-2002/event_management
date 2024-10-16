from datetime import datetime, timedelta
import random

from flask import render_template, request, jsonify, session, make_response
from flask_mail import Mail, Message
from models import User,EventOrganizer
from db import db
import os
from utils import hash_password,verify_password,send_reset_email

def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')  
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "Username, email, and password are required"}), 400
    hashpassword= hash_password(password)
    
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Username already exists"}), 409

   
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 409

    new_user = User(username=username, email=email, password=hashpassword)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    hashpassword = hash_password(password)

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

   
    user = User.query.filter_by(email=email, password=hashpassword).first()

    if user is None:
        return jsonify({"error": "Invalid email or password"}), 401

    
    return jsonify({
        "success": True,
        "message": "Login successful",
        "user": {
            "id": user.id,         
            "email": user.email,   
            "username": user.username  
        }
    }), 200

def admin_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Username and password are required"}), 400

  
    user = EventOrganizer.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"error": "Invalid username or password"}), 401

   
    # if not check_password_hash(user.password, password):
    #     return jsonify({"error": "Invalid username or password"}), 401

    return jsonify({"message": "Login successful"}), 200



def forgot_password():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"error": "Email is required"}), 400

    reset_url = "file:///C:/Users/Smita%20Sahu/Desktop/Event-Managemet/frontend/reser-password.html"

    
    send_reset_email(email, reset_url)

    return jsonify({"message": "Password reset link has been sent to your email"}), 200
