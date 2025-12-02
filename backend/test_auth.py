"""
Quick script to test authentication manually
"""
from routes.auth import get_current_user, oauth2_scheme
from database.connection import SessionLocal
from fastapi import Depends

# This will help debug auth issues
print("Testing authentication setup...")

# Check if we can import everything
print("✓ Auth routes imported successfully")
print("✓ Database connection available")

# Test token
from routes.auth import create_access_token
test_token = create_access_token(data={"sub": "jk"})
print(f"\nSample token for user 'jk':")
print(test_token)
print("\nTry this token in your browser console:")
print(f"localStorage.setItem('access_token', '{test_token}')")
