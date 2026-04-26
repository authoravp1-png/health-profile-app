from flask import Flask, request, jsonify
import requests
import uuid
import os
import jwt
import datetime
import bcrypt

app = Flask(__name__)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")  # change later

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# ------------------------
# Helper: Generate Token
# ------------------------
def generate_token(user):
    payload = {
        "abha_id": user["abha_id"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


# ------------------------
# Home
# ------------------------
@app.route("/")
def home():
    return "Health Profile API Running with Auth"


# ------------------------
# Register
# ------------------------
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    password = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt()).decode()

    user = {
        "id": str(uuid.uuid4()),
        "name": data["name"],
        "age": data["age"],
        "gender": data["gender"],
        "blood_group": data["blood_group"],
        "abha_id": data["abha_id"],
        "password": password
    }

    res = requests.post(
        f"{SUPABASE_URL}/rest/v1/users",
        json=user,
        headers=headers
    )

    if res.status_code != 201:
        return jsonify({"error": res.text}), 400

    return jsonify({"status": "registered"})


# ------------------------
# Login
# ------------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    res = requests.get(
        f"{SUPABASE_URL}/rest/v1/users?abha_id=eq.{data['abha_id']}",
        headers=headers
    )

    users = res.json()

    if len(users) == 0:
        return jsonify({"error": "User not found"}), 404

    user = users[0]

    if not bcrypt.checkpw(data["password"].encode(), user["password"].encode()):
        return jsonify({"error": "Invalid password"}), 401

    token = generate_token(user)

    return jsonify({
        "status": "success",
        "token": token
    })


# ------------------------
# Protected Route
# ------------------------
@app.route("/profile", methods=["GET"])
def profile():
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Token missing"}), 401

    try:
        token = token.split(" ")[1]
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        return jsonify({
            "message": "Access granted",
            "user": decoded
        })

    except:
        return jsonify({"error": "Invalid token"}), 401


# ------------------------
# Run
# ------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
