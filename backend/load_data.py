import pandas as pd
from sqlalchemy import create_engine

# Replace with your password
DATABASE_URL = "postgresql://postgres:gee*thU1@localhost:5432/inventory_risk_db"

engine = create_engine(DATABASE_URL)

# Load CSV
df = pd.read_csv("../data/retail_inventory.csv")

# Insert into database
df.to_sql("products", engine, if_exists="replace", index=False)

print("Data inserted successfully!")