import os
import json
import datetime
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set folder paths
RAW_DIR = r"C:\Users\khuwa\Cse_Project\coin_market_cap_top_50\March Data"
SENT_DIR = r"C:\Users\khuwa\Cse_Project\coin_market_cap_top_50\Market_Sentiment"

# Load JSON helper
def load_json(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except:
        return None

# Get sentiment by name
def get_sentiment(data, name):
    for entry in data:
        if entry["name"].lower() == name.lower():
            return entry.get("prediction")
    return None

# Collect features from all days
data_rows = []

for day in range(1, 32):
    today = datetime.datetime.strptime(f"2025-03-{day:02d}", "%Y-%m-%d")
    raw_file = os.path.join(RAW_DIR, f"data_{today.month}_{today.day:02d}_{today.year}.json")
    sent_file = os.path.join(SENT_DIR, f"market_sentiment_{today.strftime('%m_%d_%Y')}.json")

    raw_data = load_json(raw_file)
    sent_data = load_json(sent_file)

    if not raw_data or not sent_data:
        continue

    for coin in raw_data:
        name = coin["name"]
        sentiment = get_sentiment(sent_data, name)
        if sentiment is None:
            continue

        try:
            row = {
                "sentiment": sentiment,
                "price_usd": float(coin.get("price_usd", 0)),
                "market_cap": float(coin.get("market_cap_usd", 0)),
                "volume": float(coin.get("volume_24h_usd", 0)),
                "return_1h": float(coin.get("percent_change_1h", 0)),
                "return_24h": float(coin.get("percent_change_24h", 0)),
                "return_7d": float(coin.get("percent_change_7d", 0)),
            }
            
            row["volatility"] = abs(row["return_1h"]) + abs(row["return_24h"]) + abs(row["return_7d"])
            data_rows.append(row)
        except:
            continue

# Convert to DataFrame
df = pd.DataFrame(data_rows)

# Correlation matrix
corr_matrix = df.corr(numeric_only=True)

# Plot heatmap
plt.figure(figsize=(10, 7))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", center=0, linewidths=0.5)
plt.title("📊 Correlation Matrix: Sentiment vs Market Metrics", fontsize=14)
plt.tight_layout()
plt.show()
