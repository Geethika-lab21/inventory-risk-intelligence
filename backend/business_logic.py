def calculate_business_insights(product, predicted_risk):

    stock = product["stock_quantity"]
    sales = product["daily_sales"]
    expiry = product["days_to_expiry"]
    price = product["price"]

    # ---------------------------------------
    # Sell Through Rate
    # ---------------------------------------
    sell_through_rate = round((sales / stock) * 100, 2) if stock > 0 else 0

    # ---------------------------------------
    # Potential Unsold Quantity
    # ---------------------------------------
    expected_sales_before_expiry = sales * expiry
    unsold_quantity = max(stock - expected_sales_before_expiry, 0)

    # ---------------------------------------
    # Expected Revenue Loss
    # ---------------------------------------
    expected_revenue_loss = round(unsold_quantity * price, 2)

    # ---------------------------------------
    # Discount Logic (Dynamic & Realistic)
    # ---------------------------------------
    if predicted_risk == "High":

        if expiry <= 5:
            discount = 40
            urgency = "Immediate Action Required"
        elif expiry <= 10:
            discount = 30
            urgency = "High Priority"
        else:
            discount = 25
            urgency = "Monitor Closely"

        recommendation = (
            "Heavy discount + Push promotions + Stop reordering"
        )

    elif predicted_risk == "Medium":

        discount = 15
        urgency = "Moderate Risk"

        recommendation = (
            "Apply small discount + Monitor demand + Avoid excess restocking"
        )

    else:  # Low Risk

        discount = 0
        urgency = "Safe"

        recommendation = (
            "No discount needed + Maintain current inventory strategy"
        )

    return {
        "sell_through_rate": sell_through_rate,
        "expected_revenue_loss": expected_revenue_loss,
        "suggested_discount": discount,
        "urgency_level": urgency,
        "recommendation": recommendation
    }