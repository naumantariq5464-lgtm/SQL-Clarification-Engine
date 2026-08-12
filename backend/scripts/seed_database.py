import json
import os
import sys

# Add backend directory to sys.path to resolve imports properly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from app.db.database import engine, Base, SessionLocal
from app.db.models import Customer, Category, Product, Order, OrderItem, Payment

def seed_database():
    print("Creating tables in Neon PostgreSQL...")
    # Create all tables if they do not exist
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")
    
    data_file = os.path.join(os.path.dirname(__file__), "dummy_data.json")
    if not os.path.exists(data_file):
        print(f"Error: {data_file} not found. Please run generate_data.py first.")
        return
        
    with open(data_file, "r") as f:
        data = json.load(f)
        
    db = SessionLocal()
    try:
        # We will bulk insert using simple iteration (since dataset is small ~150)
        # Note: If dataset was huge, we would use db.bulk_insert_mappings()
        
        print("Inserting Categories...")
        for item in data["categories"]:
            db.merge(Category(**item))
            
        print("Inserting Customers...")
        for item in data["customers"]:
            db.merge(Customer(**item))
            
        print("Inserting Products...")
        for item in data["products"]:
            db.merge(Product(**item))
            
        print("Inserting Orders...")
        for item in data["orders"]:
            db.merge(Order(**item))
            
        print("Inserting Order Items...")
        for item in data["order_items"]:
            db.merge(OrderItem(**item))
            
        print("Inserting Payments...")
        for item in data["payments"]:
            db.merge(Payment(**item))
            
        db.commit()
        print("Database seeded successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"Error during seeding: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
