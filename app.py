from flask import Flask, jsonify, send_from_directory
import csv
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='../frontend')
CORS(app)  # Allow requests from frontend

@app.route("/api/data")
def get_data():
    data = []
    try:
        with open("data.csv", newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Convert year values to integers
                try:
                    row["2023"] = int(row["2023"])
                    row["2024"] = int(row["2024"])
                    row["2025"] = int(row["2025"])
                    data.append(row)
                except ValueError:
                    # Skip rows with invalid data
                    continue
        return jsonify(data)
    except Exception as e:
        print(f"Error loading data: {e}")
        return jsonify({"error": str(e)}), 500

# Serve the frontend
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(app.static_folder, path)

if __name__ == "__main__":
    print(f"Working directory: {os.getcwd()}")
    print(f"Looking for data.csv in: {os.path.join(os.getcwd(), 'data.csv')}")
    app.run(debug=True)