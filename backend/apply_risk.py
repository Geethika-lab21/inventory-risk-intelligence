import pandas as pd
from sqlalchemy import create_engine
from ml.risk_score import calculate_risk_score
from ml.recommendation import generate_recommendation

# 🔐 Replace with your real PostgreSQL password
DATABASE_URL = "postgresql://postgres:gee*thU1@localhost:5432/inventory_risk_db"

engine = create_engine(DATABASE_URL)

# -----------------------------
# 1️⃣ Fetch data from database
# -----------------------------
query = "SELECT * FROM products"
df = pd.read_sql(query, engine)

# -----------------------------
# 2️⃣ Apply Risk Scoring
# -----------------------------
df["risk_score"] = df.apply(
    lambda row: calculate_risk_score(
        row["stock_quantity"],
        row["daily_sales"],
        row["days_to_expiry"]
    ),
    axis=1
)

# -----------------------------
# 3️⃣ Categorize Risk
# -----------------------------
def categorize_risk(score):
    if score >= 80:
        return "High"
    elif score >= 50:
        return "Medium"
    else:
        return "Low"

df["risk_category"] = df["risk_score"].apply(categorize_risk)

# -----------------------------
# 4️⃣ Generate Recommendations
# -----------------------------
df["recommendation"] = df.apply(
    lambda row: generate_recommendation(
        row["risk_category"],
        row["stock_quantity"],
        row["daily_sales"],
        row["days_to_expiry"]
    ),
    axis=1
)

# -----------------------------
# 5️⃣ Sort by Highest Risk
# -----------------------------
df_sorted = df.sort_values(by="risk_score", ascending=False)

print("\nTop 10 High Risk Products:")
print(df_sorted[[
    "product_id",
    "product_name",
    "risk_score",
    "risk_category",
    "recommendation"
]].head(10))

# -----------------------------
# 6️⃣ Risk Distribution Summary
# -----------------------------
print("\nRisk Score Summary:")
print(df["risk_score"].describe())

print("\nRisk Category Distribution:")
print(df["risk_category"].value_counts())
# -----------------------------
# 7️⃣ Store Risk Results in Database
# -----------------------------

risk_output = df[[
    "product_id",
    "risk_score",
    "risk_category",
    "recommendation"
]]

risk_output.to_sql("product_risk", engine, if_exists="replace", index=False)

print("\nRisk results stored successfully in database.")