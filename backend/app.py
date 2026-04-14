from flask import Flask,request,jsonify
from pymongo import MongoClient
from flask_cors import CORS
from urllib.parse import quote_plus

app = Flask(__name__)
CORS(app)

username = "nandannand2003_db_user"
password = "RV/qE!s3zMq5Hr6"
encoded_password = quote_plus(password)
client = MongoClient(
    f"mongodb+srv://{username}:{encoded_password}@cluster0.p0h3vcw.mongodb.net/?appName=Cluster0"
)
db = client["mydatabase"]
collection = db["tasks"]

@app.route("/tasks",methods=["GET"])
def get_tasks():
    data=list(collection.find({},{"_id":0}))
    return jsonify(data)

@app.route("/tasks",methods=["POST"])
def add_task():
    data=request.json
    collection.insert_one(data)
    return jsonify({"message":"Task added successfully"})

@app.route("/tasks/<title>",methods=["DELETE"])
def delete_task(title):
    collection.delete_one({"title":title})
    return jsonify({"message":"Task deleted successfully"})

if __name__=="__main__":    app.run(host="0.0.0.0", port=5000)