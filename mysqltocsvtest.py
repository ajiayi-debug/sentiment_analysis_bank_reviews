import mysql.connector
import pandas as pd

# Database connection parameters
config = {
    'user': 'root',
    'password': 'JJY#91296517',
    'host': '127.0.0.1',
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
