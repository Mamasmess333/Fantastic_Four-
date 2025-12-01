import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

try:
    conn = psycopg2.connect(
        host=os.getenv("db_host"),
        port=os.getenv("db_port"),
        dbname=os.getenv("db_name"),  # or
        user=os.getenv("db_user"),
        password=os.getenv("db_pass")
    )
    print("Connected to AWS RDS PostgreSQL successfully!")
    conn.close()
except Exception as e:
    print("Connection failed:", e)
