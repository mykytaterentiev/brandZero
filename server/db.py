import psycopg2
from psycopg2 import OperationalError

# Function to connect to PostgreSQL
def create_connection():
    try:
        connection = psycopg2.connect(
            dbname="transaction_db",  # Correct database name
            user="postgres",
            password="Aqsw2143",
            host="localhost"
        )
        return connection
    except OperationalError as e:
        print(f"The error '{e}' occurred")
        return None

# Connect to the PostgreSQL database
conn = create_connection()
