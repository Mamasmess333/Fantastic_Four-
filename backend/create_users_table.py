"""
Run this script to create the users table in your database
"""
from database.connection import engine, Base
from models.user import User

def create_tables():
    print("Creating users table...")
    Base.metadata.create_all(bind=engine)
    print("Users table created successfully!")

if __name__ == "__main__":
    create_tables()
