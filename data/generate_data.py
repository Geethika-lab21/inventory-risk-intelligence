import pandas as pd
import numpy as np
import random

np.random.seed(42)

num_products = 3000

categories = ["Dairy", "Bakery", "Beverages", "Snacks", "Frozen", "Fruits", "Vegetables"]
branches = [1, 2, 3]

data = []

for i in range(num_products):
    category = random.choice(categories)

    # 70% normal products
    if random.random() < 0.7:
        daily_sales = np.random.randint(5, 40)
        stock_quantity = daily_sales * np.random.randint(3, 12)
        days_to_expiry = np.random.randint(10, 60)

    # 15% overstock disaster
    elif random.random() < 0.85:
        daily_sales = np.random.randint(1, 10)
        stock_quantity = daily_sales * np.random.randint(20, 50)
        days_to_expiry = np.random.randint(5, 20)

    # 10% near expiry crisis
    elif random.random() < 0.95:
        daily_sales = np.random.randint(5, 30)
        stock_quantity = daily_sales * np.random.randint(5, 15)
        days_to_expiry = np.random.randint(1, 5)

    # 5% dead stock
    else:
        daily_sales = np.random.randint(0, 3)
        stock_quantity = np.random.randint(200, 500)
        days_to_expiry = np.random.randint(1, 30)

    price = round(np.random.uniform(10, 500), 2)
    branch_id = random.choice(branches)

    data.append([
        i,
        f"Product_{i}",
        category,
        stock_quantity,
        daily_sales,
        days_to_expiry,
        price,
        branch_id
    ])

columns = [
    "product_id",
    "product_name",
    "category",
    "stock_quantity",
    "daily_sales",
    "days_to_expiry",
    "price",
    "branch_id"
]

df = pd.DataFrame(data, columns=columns)

df.to_csv("inventory_risk_system/data/retail_inventory.csv", index=False)

print("Improved dataset generated successfully!")