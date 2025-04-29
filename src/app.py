from flask import Flask, request, jsonify
import threading
import requests
import time
import os
from cryptography.fernet import Fernet
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

ENCR_KEY = os.getenv('ENCR_KEY')

if not ENCR_KEY:
    raise ValueError("ENCR_KEY environment variable is not set!")

cipher = Fernet(ENCR_KEY)

# heartbeat stuff
heartbeat_started = False

def send_heartbeat():
    while True:
        try:
            requests.get("https://ns-api-970c.onrender.com/")
            print("Heartbeat sent")
        except requests.exceptions.RequestException as e:
            print(f"Error sending heartbeat: {e}")
        time.sleep(10)

@app.before_request
def start_heartbeat():
    global heartbeat_started
    if not heartbeat_started:
        heartbeat_started = True
        heartbeat_thread = threading.Thread(target=send_heartbeat)
        heartbeat_thread.daemon = True
        heartbeat_thread.start()

@app.route('/api/account/create', methods=['POST'])
def create_account():
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    
    encrypted_password = cipher.encrypt(password.encode('utf-8')).decode('utf-8')

    new_user = User(username=username, password=encrypted_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Account created successfully!"}), 201

@app.route('/api/account/login', methods=['POST'])
def login():
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()

    if user:
        decrypted_password = cipher.decrypt(user.password.encode('utf-8')).decode('utf-8')

        if decrypted_password == password:
            return jsonify({"message": "Login successful!"}), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401
    else:
        return jsonify({"error": "Invalid username or password"}), 401

@app.route('/')
def home():
    return "Hello, World!"

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)