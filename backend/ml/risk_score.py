import pandas as pd
def calculate_risk_score(stock_quantity, daily_sales, days_to_expiry):

    # Avoid division errors
    daily_sales = max(daily_sales, 1)

    # How many days stock will last
    stock_days_remaining = stock_quantity / daily_sales

    # Risk increases if stock lasts longer than expiry window
    pressure_ratio = stock_days_remaining / max(days_to_expiry, 1)

    # Log scaling for realism
    import math
    pressure_score = min(math.log1p(pressure_ratio) / 3, 1)

    # Expiry urgency
    expiry_score = 1 - min(days_to_expiry / 60, 1)

    final_score = (0.6 * pressure_score + 0.4 * expiry_score) * 100

    return round(final_score, 2)