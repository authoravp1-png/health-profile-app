from flask import Flask, request, jsonify
import requests
import uuid
import os

app = Flask(__name__)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

@app.route("/")
def home():
    return "Health Profile API Running"

@app.route("/create_user", methods=["GET", "POST"])
def create_user():
    if request.method == "GET":
        return "Use POST method to create user"


    
    data = request.json

    user = {
        "id": str(uuid.uuid4()),
        "name": data["name"],
        "age": data["age"],
        "gender": data["gender"],
        "blood_group": data["blood_group"],
        "abha_id": data["abha_id"]
    }

    res = requests.post(
        f"{SUPABASE_URL}/rest/v1/users",
        json=user,
        headers=headers
    )

    return jsonify(res.json())

app.run(host="0.0.0.0", port=5000)
