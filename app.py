from flask import Flask, jsonify
from flask_mysqldb import MySQL
import json
import mysql.connector

app = Flask(__name__)

# Load configuration from JSON file
with open('config.json') as config_file:
    config = json.load(config_file)

@app.route('/')
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
        cursor.execute("SELECT * FROM combined_reviews")
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

if __name__ == '__main__':
    app.run(debug=True)


