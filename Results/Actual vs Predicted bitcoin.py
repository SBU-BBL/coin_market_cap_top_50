import os
import json
import datetime
import matplotlib.pyplot as plt

#FILE PATHS
RAW_DIR = r"C:\Users\khuwa\Cse_Project\coin_market_cap_top_50\March Data"
PRED_DIR = r"C:\Users\khuwa\Cse_Project\coin_market_cap_top_50\Predicted_Price"

# === Load JSON ===
def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return None

#Data Storage
dates = []
actual_prices = []
predicted_prices = []

#Loop March 1 to 30
for day in range(1, 31):
    today = datetime.datetime.strptime(f"2025-03-{day:02d}", "%Y-%m-%d")
    tomorrow = today + datetime.timedelta(days=1)

    d1 = f"{today.month}_{today.day:02d}_{today.year}"       # For raw data file
    d2 = tomorrow.strftime("%m_%d_%Y")                        # For predicted data file

    raw_file = os.path.join(RAW_DIR, f"data_{d1}.json")
    pred_file = os.path.join(PRED_DIR, f"predicted_prices_{d2}.json")

    raw_data = load_json(raw_file)
    pred_data = load_json(pred_file)

    if not raw_data or not pred_data:
        continue

    # Get Bitcoin prices
    btc_actual = next((coin for coin in raw_data if coin["name"].lower() == "bitcoin"), None)
    btc_pred = next((coin for coin in pred_data if coin["name"].lower() == "bitcoin"), None)

    if btc_actual and btc_pred:
        dates.append(tomorrow.strftime("%b %d"))  # Show predicted date
        actual_prices.append(float(btc_actual.get("price_usd", 0)))
        predicted_prices.append(float(btc_pred.get("predicted_price_usd", 0)))

#Plotting
plt.figure(figsize=(12, 6))
plt.plot(dates, actual_prices, label="Actual Bitcoin Price", marker='o')
plt.plot(dates, predicted_prices, label="Predicted Bitcoin Price", marker='x')
plt.xticks(rotation=45)
plt.title("Bitcoin: Actual vs Predicted Price (March 2025)")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
