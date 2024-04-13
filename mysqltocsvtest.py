import mysql.connector
import pandas as pd

# Database connection parameters
config = {
    'user': 'root',
    'password': 'SQL12345',
    'host': 'ec2-54-254-215-140.ap-southeast-1.compute.amazonaws.com',
    'database': 'database',
}

# Establish a connection
cnx = mysql.connector.connect(**config)

# Define your query
query = f"SELECT * FROM combined_reviews"

# Use pandas to load sql query into a DataFrame
df = pd.read_sql(query, con=cnx)

print(df.head())  # Print the first few rows of the DataFrame

# Don't forget to close the connection when done
cnx.close()
