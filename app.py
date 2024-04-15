from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

@app.route('/')
def index():
    try:
        # Connect to the MySQL database with SSL
        connection = mysql.connector.connect(
            host='ec2-13-212-240-70.ap-southeast-1.compute.amazonaws.com',
            user='root',
            password='SQL12345',
            database='database',
            ssl_ca='./dsa-3101-2320-project.pem'  # Path to your SSL certificate
        )
        cursor = connection.cursor()

        # Execute a query
        cursor.execute("SELECT * FROM combined_reviews")
        row_headers = [x[0] for x in cursor.description]  # Extract row headers for JSON keys
        rv = cursor.fetchall()
        cursor.close()
        connection.close()  # Close the connection

        # Transform query results into a list of dictionaries
        json_data = [dict(zip(row_headers, result)) for result in rv]
        return jsonify(json_data)

    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

