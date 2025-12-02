"""
Script to view all users in the database
"""
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from models.user import User
from datetime import datetime

def view_users():
    db = SessionLocal()
    try:
        users = db.query(User).all()

        if not users:
            print("No users found in the database.")
            return

        print(f"\n{'='*80}")
        print(f"Total Users: {len(users)}")
        print(f"{'='*80}\n")

        for user in users:
            print(f"ID:           {user.id}")
            print(f"Username:     {user.username}")
            print(f"Email:        {user.email}")
            print(f"Created At:   {user.created_at}")
            print(f"Password:     {'*' * 20} (hashed)")
            print("-" * 80)

    finally:
        db.close()

if __name__ == "__main__":
    view_users()
