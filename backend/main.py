from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
import pandas as pd
import joblib
from business_logic import calculate_business_insights

# ============================================================
# 🔹 App Initialization
# ============================================================

app = FastAPI(
    title="Inventory Risk & Decision Intelligence API",
    version="1.0"
)

# ============================================================
# 🔹 CORS Configuration (React Frontend)
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# 🔹 Database Configuration
# ============================================================

DATABASE_URL = "postgresql+psycopg2://postgres:gee*thU1@localhost:5432/inventory_risk_db"
engine = create_engine(DATABASE_URL)

# ============================================================
# 🔹 Load Trained ML Model
# ============================================================

model = joblib.load("ml/inventory_risk_model.pkl")

# ============================================================
# 🔹 Root Endpoint
# ============================================================

@app.get("/")
def home():
    return {
        "message": "Inventory Expiry Risk & Decision Intelligence API is running"
    }

# ============================================================
# 🔹 Predict Risk (ML Only)
# ============================================================

@app.get("/predict/{product_id}")
def predict_risk(product_id: int):

    query = text("""
        SELECT stock_quantity, daily_sales, days_to_expiry
        FROM products
        WHERE product_id = :pid
    """)

    df = pd.read_sql(query, engine, params={"pid": product_id})

    if df.empty:
        raise HTTPException(status_code=404, detail="Product not found")

    prediction = model.predict(df)[0]

    probabilities = model.predict_proba(df)[0]
    class_labels = model.classes_
    class_probs = dict(zip(class_labels, probabilities))

    confidence = float(class_probs[prediction])

    return {
        "product_id": product_id,
        "predicted_risk_category": prediction,
        "confidence_score": round(confidence, 3),
        "class_probabilities": {
            k: round(float(v), 3)
            for k, v in class_probs.items()
        }
    }

# ============================================================
# 🔹 Full Product Intelligence (ML + Business Logic)
# ============================================================

@app.get("/product-insights/{product_id}")
def product_insights(product_id: int):

    query = text("""
        SELECT product_id,
               product_name,
               stock_quantity,
               daily_sales,
               days_to_expiry,
               price
        FROM products
        WHERE product_id = :pid
    """)

    df = pd.read_sql(query, engine, params={"pid": product_id})

    if df.empty:
        raise HTTPException(status_code=404, detail="Product not found")

    features = df[["stock_quantity", "daily_sales", "days_to_expiry"]]

    predicted_risk = model.predict(features)[0]

    probabilities = model.predict_proba(features)[0]
    class_labels = model.classes_
    class_probs = dict(zip(class_labels, probabilities))

    confidence = float(class_probs[predicted_risk])

    product_data = df.iloc[0].to_dict()

    business_data = calculate_business_insights(
        product_data,
        predicted_risk
    )

    return {
        "product_id": product_id,
        "product_name": product_data["product_name"],
        "predicted_risk_category": predicted_risk,
        "confidence_score": round(confidence, 3),
        "class_probabilities": {
            k: round(float(v), 3)
            for k, v in class_probs.items()
        },
        **business_data
    }

# ============================================================
# 🔹 Dashboard Summary (All Products - Optimized)
# ============================================================

@app.get("/dashboard-summary")
def dashboard_summary():

    query = """
        SELECT product_id,
               product_name,
               stock_quantity,
               daily_sales,
               days_to_expiry,
               price
        FROM products
    """

    df = pd.read_sql(query, engine)

    if df.empty:
        raise HTTPException(status_code=404, detail="No products found")

    # 🔹 Vectorized Prediction (FAST)
    features = df[["stock_quantity", "daily_sales", "days_to_expiry"]]

    predicted_risks = model.predict(features)
    probabilities = model.predict_proba(features)
    confidences = probabilities.max(axis=1)

    results = []

    for idx in range(len(df)):

        product_data = df.iloc[idx].to_dict()

        business_data = calculate_business_insights(
            product_data,
            predicted_risks[idx]
        )

        results.append({
            "product_id": product_data["product_id"],
            "product_name": product_data["product_name"],
            "risk": predicted_risks[idx],
            "confidence": round(float(confidences[idx]), 3),
            "expected_loss": business_data["expected_revenue_loss"],
            "urgency_level": business_data["urgency_level"]
        })

    return results