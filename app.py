from flask import Flask, request, jsonify
import requests
import uuid
import os

app = Flask(__name__)

# Environment variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# ------------------------
# Home Route
# ------------------------
@app.route("/")
def home():
    return jsonify({
        "message": "Health Profile API Running",
        "endpoints": {
            "POST /create_user": "Create new user",
            "GET /get_users": "Fetch all users"
        }
    })


# ------------------------
# Create User
# ------------------------
@app.route("/create_user", methods=["GET", "POST"])
def create_user():

    # Browser test
    if request.method == "GET":
        return jsonify({"message": "Use POST method to create user"})

    data = request.get_json()

    # Validation
    required_fields = ["name", "age", "gender", "blood_group", "abha_id"]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    user = {
        "id": str(uuid.uuid4()),
        "name": data["name"],
        "age": data["age"],
        "gender": data["gender"],
        "blood_group": data["blood_group"],
        "abha_id": data["abha_id"]
    }

    try:
        res = requests.post(
            f"{SUPABASE_URL}/rest/v1/users",
            json=user,
            headers=headers
        )

        if res.status_code != 201:
            return jsonify({"error": res.text}), 400

        return jsonify({
            "status": "success",
            "user": user
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ------------------------
# Get All Users
# ------------------------
@app.route("/get_users", methods=["GET"])
def get_users():

    try:
        res = requests.get(
            f"{SUPABASE_URL}/rest/v1/users",
            headers=headers
        )

        return jsonify(res.json())

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ------------------------
# Register
# ------------------------
@app.route("/register", methods=["GET", "POST"])
def create_user():

    # Browser test
    if request.method == "GET":
        return jsonify({"message": "Use POST method to create user"})

    data = request.get_json()

    # Validation
    required_fields = ["name", "age", "gender", "blood_group", "abha_id"]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    user = {
        "id": str(uuid.uuid4()),
        "name": data["name"],
        "age": data["age"],
        "gender": data["gender"],
        "blood_group": data["blood_group"],
        "abha_id": data["abha_id"]
    }

    try:
        res = requests.post(
            f"{SUPABASE_URL}/rest/v1/users",
            json=user,
            headers=headers
        )

        if res.status_code != 201:
            return jsonify({"error": res.text}), 400

        return jsonify({
            "status": "success",
            "user": user
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500



# ------------------------
# Health Check
# ------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/update_user", methods=["PUT"])
def update_user():
    data = request.get_json()

    res = requests.patch(
        f"{SUPABASE_URL}/rest/v1/users?abha_id=eq.{data['abha_id']}",
        json=data,
        headers=headers
    )

    return jsonify({"status": "updated"})
    
# ------------------------
# Run App (for local)
# ------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
