from flask import Flask, jsonify, render_template
import subprocess
from pymongo import MongoClient


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run-script", methods=["GET"])
def run_script():
    subprocess.run(["python", "scrape_twitter_trends.py"])  

    client = MongoClient('mongodb://localhost:27017/')
    db = client["twitter_trends"]  # Replace with your actual database name
    collection = db["trends"]  # Replace with your actual collection name

    latest_record = collection.find().sort("timestamp", -1).limit(1)
    if latest_record:
        return jsonify(latest_record)
    return jsonify({"error": "No data found."})

if __name__ == "__main__":
    app.run(debug=True)
