from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from db import db
import secrets
import jwt
import os
from dotenv import load_dotenv
from flask_cors import CORS
# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data['username']
    password = data['password']

    if not username or not password:
        return jsonify({'message': 'Username and password are required.'}), 400
    
    existing_user = db.users_collection.find_one({'username': username})
    if existing_user:
        return jsonify({'message': 'Username already exists. Please choose a different username.'}), 400
    
    hashed_password = generate_password_hash(password)
    db.users_collection.insert_one({'username': username, 'password': hashed_password})
    print('succesful')
    return jsonify({'message': 'User registered successfully.'}), 201

@app.route('/signin', methods=['POST'])
def signin():
    data = request.json
    username = data.get('username')  # Use .get() to avoid KeyError if 'username' is missing
    password = data.get('password')  # Use .get() to avoid KeyError if 'password' is missing

    if not username or not password:
        return jsonify({'message': 'Username and password are required.'}), 400
    
    user = db.users_collection.find_one({'username': username})
    if not user or not check_password_hash(user['password'], password):
        return jsonify({'message': 'Invalid username or password.'}), 401
    
    # Generate a JWT token with the user's ID (you can include more data if needed)
    token = jwt.encode({'username': str(user['username'])}, app.config['SECRET_KEY'], algorithm='HS256')
    
    # Return the JWT token in the response along with a success message
    print(token)
    return jsonify({'message': 'Sign-in successful!', 'token': token}), 200

@app.route('/check_connection')
def check_connection():
    try:
        # Get server status
        server_status = db.get_server_status()  # Attempt to query MongoDB server info
        return jsonify({'message': 'Database connection successful!','server-status':str(server_status)}), 200
    except Exception as e:
        return jsonify({'message': 'Database connection error.', 'error': str(e)}), 500

if __name__ == '__main__':
    port = 5000  # Choose the port number you want to use
    app.run(debug=True, port=port)
    print(f"Server is running on port {port}")