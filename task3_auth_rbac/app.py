import datetime
import jwt
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'szabist_secret_key_2026'

# Classroom Mock DB (User credentials & Roles)
USERS = {
    "student_user": {"password": "user123", "role": "User"},
    "admin_user": {"password": "admin123", "role": "Admin"}
}

# Helper Function: Token Validation
def verify_token():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return None, jsonify({"error": "Unauthorized: Token missing or invalid header format"}), 401
    
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        return payload, None, 200
    except jwt.ExpiredSignatureError:
        return None, jsonify({"error": "Unauthorized: Token has expired"}), 401
    except jwt.InvalidTokenError:
        return None, jsonify({"error": "Unauthorized: Invalid token"}), 401

# --- ENDPOINTS ---

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Bad Request: Username and password required"}), 400
    
    username = data['username']
    password = data['password']
    
    user = USERS.get(username)
    if not user or user['password'] != password:
        return jsonify({"error": "Unauthorized: Invalid username or password"}), 401
    
    # Generate JWT payload (expires in 1 hour)
    token_payload = {
        "username": username,
        "role": user['role'],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(token_payload, app.config['SECRET_KEY'], algorithm="HS256")
    
    return jsonify({
        "message": "Login successful",
        "token": token,
        "role": user['role']
    }), 200

@app.route('/public', methods=['GET'])
def public_route():
    return jsonify({"message": "Public Route: Open access for everyone"}), 200

@app.route('/dashboard', methods=['GET'])
def dashboard_route():
    payload, error_response, status = verify_token()
    if error_response:
        return error_response, status
    
    return jsonify({
        "message": f"Welcome to User Dashboard, {payload['username']}!",
        "role": payload['role']
    }), 200

@app.route('/admin', methods=['GET'])
def admin_route():
    payload, error_response, status = verify_token()
    if error_response:
        return error_response, status
    
    if payload.get('role') != 'Admin':
        return jsonify({"error": "Forbidden: Access Denied! Admin role required."}), 403
    
    return jsonify({
        "message": f"Welcome to Admin Panel, {payload['username']}!",
        "access": "Full Administrative Privileges Granted"
    }), 200

if __name__ == '__main__':
    print("==========================================")
    print(">>> TASK 3 JWT AUTH & RBAC SERVER LIVE <<<")
    print("==========================================")
    app.run(debug=True, port=5000)