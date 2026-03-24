
# 📦 Inventory Risk Intelligence System

An AI-powered full-stack system that predicts inventory expiry risk and provides actionable business insights to minimize revenue loss and optimize inventory decisions.

---

## 🚀 Overview

Inventory mismanagement leads to product expiry, wastage, and financial loss.
This project solves that by combining Machine Learning, backend APIs, and an interactive dashboard to provide real-time decision intelligence.

The system predicts whether a product is at High, Medium, or Low risk of expiry and recommends actions such as discounts, promotions, or stock control.

---

## ✨ Features

* Predicts inventory expiry risk (High / Medium / Low)
* Calculates expected revenue loss
* Suggests discounts and business actions
* Interactive dashboard with charts and filters
* Real-time product analysis via API
* Business-focused decision support system

---

## 🧠 Tech Stack

Frontend

* React (Vite)
* Recharts

Backend

* FastAPI (Python)
* REST API

Database

* PostgreSQL

Machine Learning

* Scikit-learn (Decision Tree Classifier)

---

## 📊 Dashboard Features

* Risk Distribution Pie Chart
  Visualizes High / Medium / Low risk products

* Top Loss Products Bar Chart
  Shows products causing highest expected revenue loss

* Risk Filtering
  Filter products by risk category

* Product Analysis
  Enter Product ID to get:

  * Risk prediction
  * Confidence score
  * Expected revenue loss
  * Suggested discount
  * Urgency level
  * Business recommendation

---

## 🧠 Machine Learning Model

Model: Decision Tree Classifier

Features used:

* Stock Quantity
* Daily Sales
* Days to Expiry

Output:

* Risk Category (High / Medium / Low)

Performance:

* Accuracy ~95%

---

## 💼 Business Logic Layer

The system provides actionable insights such as:

* Expected Revenue Loss
* Suggested Discount Strategy
* Urgency Level
* Action Recommendation

Example:

* High Risk → Heavy discount + promotions
* Medium Risk → Moderate discount
* Low Risk → No action needed

---

## 🗄️ Dataset

The dataset is synthetically generated to simulate real-world inventory conditions.

Features include:

* product_id
* product_name
* stock_quantity
* daily_sales
* days_to_expiry
* price
* risk_category

This allows testing realistic business scenarios and edge cases.

---

## ⚙️ How to Run Locally

Clone the repository:
git clone [https://github.com/Geethika-lab21/inventory-risk-intelligence.git](https://github.com/Geethika-lab21/inventory-risk-intelligence.git)
cd inventory-risk-intelligence

---

Backend setup:
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload

Backend runs at:
[http://127.0.0.1:8000](http://127.0.0.1:8000)

Swagger API docs:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

Frontend setup:
cd frontend
npm install
npm run dev

Frontend runs at:
[http://localhost:5173](http://localhost:5173)

---

## 🌐 API Endpoints

Predict Risk
GET /predict/{product_id}

Product Insights
GET /product-insights/{product_id}

Dashboard Summary
GET /dashboard-summary

---

## 📊 Visualization

* Pie chart for risk distribution
* Bar chart for top loss products
* Color-coded UI for decision making

---

## 💡 Business Impact

This system helps businesses:

* Reduce inventory wastage
* Minimize revenue loss
* Optimize pricing strategies
* Improve stock management
* Enable data-driven decisions

---

## 🚀 Future Enhancements

* Power BI integration for advanced analytics
* Cloud deployment (Vercel + Render)
* Advanced ML models (Random Forest, XGBoost)
* User authentication system
* Integration with ERP systems

---

## 👩‍💻 Author

Geethika

---

## ⭐ Final Note

This project demonstrates how Machine Learning, full-stack development, and business logic can be combined to solve real-world inventory problems.

---

If you want next step:
👉 I can help you deploy this live (so you get a working link on your resume)
