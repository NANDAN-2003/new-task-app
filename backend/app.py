from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from urllib.parse import quote_plus

app = Flask(__name__)
CORS(app)


username = "nandannand2003_db_user"
password = "Test@123"
encoded_password = quote_plus(password)

client = MongoClient(
    f"mongodb+srv://{username}:{encoded_password}@cluster0.p0h3vcw.mongodb.net/?appName=Cluster0"
)

db = client["mydatabase"]
collection = db["tasks"]

@app.route("/")
def home():
    return "Server working"


@app.route("/tasks", methods=["GET", "POST"])
@app.route("/tasks/", methods=["GET", "POST"])
def handle_tasks():
    if request.method == "GET":
        try:
            data = list(collection.find({}, {"_id": 0}))
            return jsonify(data)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    elif request.method == "POST":
        try:
            data = request.json
            collection.insert_one(data)
            return jsonify({"message": "Task added successfully"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@app.route("/tasks/<title>", methods=["DELETE"])
@app.route("/tasks/<title>/", methods=["DELETE"])
def delete_task(title):
    try:
        collection.delete_one({"title": title})
        return jsonify({"message": "Task deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
