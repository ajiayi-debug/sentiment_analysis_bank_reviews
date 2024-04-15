#This py teaches you how to retrieve the data from mysql. TAKE NOTE THAT HOST CHANGES EVERYTIME U START AND STOP THE SERVER (EVEN IN MYSQL WORKBENCH) SO EDIT IT!!!!
import mysql.connector
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
# Database connection parameters
user = 'root'
password = 'SQL12345'
host = 'ec2-13-212-240-70.ap-southeast-1.compute.amazonaws.com'
database = 'database'
connection_string = f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"

# Create an SQLAlchemy engine
engine = create_engine(connection_string)

# Define your query
query = "SELECT * FROM combined_reviews"

# Use pandas to load sql query into a DataFrame
dataset = pd.read_sql(query, con=engine)

# Convert DataFrame to CSV
dataset.to_csv('combined_reviews.csv')

# Close the engine connection when done
engine.dispose()