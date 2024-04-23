from flask import Flask, jsonify, request
import json
import mysql.connector
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import pandas as pd
from sqlalchemy import create_engine
import subprocess

app = Flask(__name__)
CORS(app)

### get customer reviews

# Load configuration from JSON file
with open('config.json') as config_file:
    config = json.load(config_file)

@app.route('/customer_review')
def index():
    try:
        # Connect to the MySQL database using values from the configuration file
        connection = mysql.connector.connect(
            host=config['database']['host'],
            user=config['database']['user'],
            password=config['database']['password'],
            database=config['database']['database'],
            port=config['database']['port']
        )
        cursor = connection.cursor()

        # Execute a query
        cursor.execute("SELECT * FROM sentiment_data")
        row_headers = [x[0] for x in cursor.description]  # Extract row headers for JSON keys
        rv = cursor.fetchall()
        cursor.close()
        connection.close()  # Ensure the connection is closed

        # Transform query results into a list of dictionaries
        json_data = [dict(zip(row_headers, result)) for result in rv]
        return jsonify(json_data)

    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

### upload csv with new data
    
database_config = config['database']

# Use the loaded configuration to create the SQLAlchemy DATABASE_URI
DATABASE_URI = f"mysql+mysqlconnector://{database_config['user']}:{database_config['password']}@{database_config['host']}:{database_config['port']}/{database_config['database']}"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URI)

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'csvFile' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['csvFile']

    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'No selected file or file type not allowed'}), 400

    # Read the CSV file directly into a Pandas DataFrame
    df = pd.read_csv(file.stream)

    # Insert the DataFrame into the MySQL database
    # Replace 'your_table_name' with your actual table name
    df.to_sql('new_data', con=engine, if_exists='append', index=False)
    
    return jsonify({'message': 'File processed and data inserted into MySQL'}), 200

### get summary data

@app.route('/summary')
def get_summary():
    try:
        # Connect to the MySQL database using values from the configuration file
        connection = mysql.connector.connect(
            host=config['database']['host'],
            user=config['database']['user'],
            password=config['database']['password'],
            database=config['database']['database'],
            port=config['database']['port']
        )
        cursor = connection.cursor()

        # Execute a query
        cursor.execute("SELECT * FROM summary")
        row_headers = [x[0] for x in cursor.description]  # Extract row headers for JSON keys
        rv = cursor.fetchall()
        cursor.close()
        connection.close()  # Ensure the connection is closed

        # Transform query results into a list of dictionaries
        json_data = [dict(zip(row_headers, result)) for result in rv]
        return jsonify(json_data)

    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

### run script on new data
    
@app.route("/new_data", methods=['GET'])
def new_data():
    try:
        result = subprocess.run(
            ['python', 'backend/newdata.py'],  # CHANGE PYTHON
            check=True,  
            capture_output=True,  
            text=True  
        )

        return jsonify({
            "message": "File processed successfully!",
            "script_output": result.stdout  
        }), 200

    except subprocess.CalledProcessError as e:
        return jsonify({
            "error": "Processing failed",
            "details": e.stderr  
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)

