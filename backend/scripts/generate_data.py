import json
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

def generate_data():
    num_customers = 10
    num_categories = 5
    num_products = 20
    num_orders = 50
    num_order_items = 150
    num_payments = 50

    customers = []
    for i in range(1, num_customers + 1):
        customers.append({
            "id": i,
            "name": fake.name(),
            "email": fake.unique.email(),
            "city": fake.city(),
            "country": fake.country(),
            "created_at": fake.date_time_between(start_date="-2y", end_date="now").isoformat()
        })

    categories = []
    category_names = ["Electronics", "Clothing", "Home & Kitchen", "Sports", "Books"]
    for i in range(1, num_categories + 1):
        categories.append({
            "id": i,
            "name": category_names[i-1]
        })

    products = []
    for i in range(1, num_products + 1):
        products.append({
            "id": i,
            "name": fake.word().capitalize() + " " + fake.word().capitalize(),
            "category_id": random.randint(1, num_categories),
            "price": round(random.uniform(10.0, 500.0), 2),
            "stock": random.randint(0, 100),
            "created_at": fake.date_time_between(start_date="-2y", end_date="now").isoformat()
        })

    orders = []
    for i in range(1, num_orders + 1):
        orders.append({
            "id": i,
            "customer_id": random.randint(1, num_customers),
            "total_amount": 0.0, # Will be calculated later
            "status": random.choice(["pending", "processing", "completed", "cancelled"]),
            "created_at": fake.date_time_between(start_date="-1y", end_date="now").isoformat()
        })

    order_items = []
    for i in range(1, num_order_items + 1):
        order_id = random.randint(1, num_orders)
        product = random.choice(products)
        quantity = random.randint(1, 5)
        unit_price = product["price"]
        
        # Add to order total
        orders[order_id - 1]["total_amount"] += round(quantity * unit_price, 2)
        
        order_items.append({
            "id": i,
            "order_id": order_id,
            "product_id": product["id"],
            "quantity": quantity,
            "unit_price": unit_price
        })

    payments = []
    for i in range(1, num_payments + 1):
        order = random.choice(orders)
        payments.append({
            "id": i,
            "order_id": order["id"],
            "amount": order["total_amount"],
            "payment_method": random.choice(["credit_card", "paypal", "bank_transfer"]),
            "status": "completed",
            "paid_at": (datetime.fromisoformat(order["created_at"]) + timedelta(days=random.randint(1, 5))).isoformat()
        })

    data = {
        "customers": customers,
        "categories": categories,
        "products": products,
        "orders": orders,
        "order_items": order_items,
        "payments": payments
    }
    
    import os
    file_path = os.path.join(os.path.dirname(__file__), "dummy_data.json")
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
        
    print(f"Data generated successfully and saved to {file_path}")

if __name__ == "__main__":
    generate_data()
