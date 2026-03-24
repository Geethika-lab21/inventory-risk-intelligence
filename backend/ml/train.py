import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

DATABASE_URL = "postgresql://postgres:gee*thU1@localhost:5432/inventory_risk_db"

engine = create_engine(DATABASE_URL)

# --------------------------------
# 1️⃣ Load Data
# --------------------------------
query = """
SELECT p.stock_quantity,
       p.daily_sales,
       p.days_to_expiry,
       r.risk_category
FROM products p
JOIN product_risk r
ON p.product_id = r.product_id
"""

df = pd.read_sql(query, engine)

print("\nDataset Loaded:")
print(df.head())

# --------------------------------
# 2️⃣ Prepare Features & Target
# --------------------------------
X = df[["stock_quantity", "daily_sales", "days_to_expiry"]]
y = df["risk_category"]

# --------------------------------
# 3️⃣ Train-Test Split
# --------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# --------------------------------
# 4️⃣ Train Random Forest Model
# --------------------------------
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=6,              # prevents overfitting
    min_samples_split=10,
    min_samples_leaf=5,
    random_state=42
)

model.fit(X_train, y_train)

# --------------------------------
# 5️⃣ Evaluate Model
# --------------------------------
y_pred = model.predict(X_test)

print("\nModel Performance:\n")
print(classification_report(y_test, y_pred))
print("Accuracy:", accuracy_score(y_test, y_pred))

# --------------------------------
# 6️⃣ Save Model
# --------------------------------
joblib.dump(model, "inventory_risk_model.pkl")

print("\nModel saved as inventory_risk_model.pkl")