#!/usr/bin/env python3
"""Quick script to view all users in the database."""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from backend.services.db_service import User, get_session
import json

def view_all_users():
    """Print all users in a readable format."""
    with get_session() as session:
        users = session.query(User).order_by(User.created_at.desc()).all()
        
        if not users:
            print("📭 No users found in database.")
            return
        
        print(f"\n👥 Found {len(users)} user(s):\n")
        print("=" * 80)
        
        for user in users:
            print(f"\n🆔 User ID: {user.id}")
            print(f"   Name: {user.name}")
            print(f"   Email: {user.email}")
            print(f"   Goal: {user.goal}")
            print(f"   Budget: ${user.budget_min:.2f} - ${user.budget_max:.2f}")
            print(f"   Dietary Preferences: {', '.join(user.dietary_preferences) if user.dietary_preferences else 'None'}")
            print(f"   Allergies: {', '.join(user.allergies) if user.allergies else 'None'}")
            print(f"   Language: {user.language}")
            print(f"   Created: {user.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print("-" * 80)

if __name__ == "__main__":
    view_all_users()

