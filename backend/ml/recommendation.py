def generate_recommendation(risk_category, stock_quantity, daily_sales, days_to_expiry):
    
    if risk_category == "High":
        if days_to_expiry <= 5:
            return "Urgent 25% discount + Promote heavily + Stop restocking"
        elif stock_quantity > daily_sales * 20:
            return "Apply 15% discount + Bundle with fast-moving item"
        else:
            return "Apply 10% discount + Monitor daily"

    elif risk_category == "Medium":
        if stock_quantity > daily_sales * 10:
            return "Small 5-10% discount + Monitor weekly"
        else:
            return "Monitor sales trend"

    else:
        return "No action required"