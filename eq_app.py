from flask import Flask, request, jsonify, render_template
import os
import csv
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["ALLOWED_EXTENSIONS"] = {"pdf"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

# Read company names from CSV file
company_names = []

with open("./eq_research/data/output/final/aggregated-tmp.csv", mode="r", encoding="utf-8") as csvfile:
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        company_names.append(row["name"])

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files["file"]
    
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400
    
    filename = secure_filename(file.filename)

    return jsonify({"companies": company_names})

def get_company_data(company_name):
    with open("./eq_research/data/output/final/aggregated-tmp.csv", mode="r", encoding="utf-8") as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            if row["name"] == company_name:
                renamed_data = {
                    "Company": row["name"],                    
                    "Fair Value": row["fair_value"],
                    "Uncertainity": row["uncertainity"],
                    "Consider Buy at": row["consider_buy"],
                    "Consider Sell at": row["consider_sell"],
                    "Bullish Views": row["bullish_views"],
                    "Bearish Views": row["bearish_views"],
                    "Macro Views": row["macro_views"],
                    "Interesting Numbers": row["interesting_numbers"],
                    
                }

                # Remove empty values from the dictionary
                filtered_data = {k: v for k, v in renamed_data.items() if v}

                return filtered_data
    return None



@app.route("/analyse", methods=["POST"])
def analyse():
    company = request.form.get("company")

    if not company:
        return jsonify({"error": "No company provided"}), 400

    company_data = get_company_data(company)

    if not company_data:
        return jsonify({"error": "Company not found"}), 404

    return jsonify(company_data)

if __name__ == "__main__":
    app.run(debug=True ,port=7777)
