#!/usr/bin/env python3
"""
Script to create a test user for login testing
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.models import User, Base
from backend.app.auth import get_password_hash

# Database setup
DATABASE_URL = "sqlite:///./unified_portal.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_test_user():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if test user already exists
        existing_user = db.query(User).filter(User.email == "test@example.com").first()
        if existing_user:
            print("✅ Test user already exists:")
            print(f"   Email: {existing_user.email}")
            print(f"   Name: {existing_user.full_name}")
            print(f"   Mobile: {existing_user.mobile}")
            return
        
        # Create test user
        test_user = User(
            email="test@example.com",
            mobile="9999999999",
            hashed_password=get_password_hash("test123"),
            full_name="Test User",
            city="Ahmedabad"
        )
        
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        print("✅ Test user created successfully!")
        print(f"   Email: {test_user.email}")
        print(f"   Password: test123")
        print(f"   Name: {test_user.full_name}")
        print(f"   Mobile: {test_user.mobile}")
        
    except Exception as e:
        print(f"❌ Error creating test user: {e}")
        db.rollback()
    finally:
        db.close()

def list_all_users():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        if not users:
            print("❌ No users found in database")
            return
        
        print(f"📋 Found {len(users)} users:")
        for user in users:
            print(f"   ID: {user.id}, Email: {user.email}, Name: {user.full_name}")
            
    except Exception as e:
        print(f"❌ Error listing users: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🔍 Checking database users...")
    list_all_users()
    print("\n🔧 Creating test user...")
    create_test_user()