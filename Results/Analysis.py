import os
import json
import datetime
from collections import defaultdict, Counter
import pandas as pd

#FILE PATHs
RAW_DIR = r"C:\Users\khuwa\Cse_Project\coin_market_cap_top_50\March Data"
PRED_DIR = r"C:\Users\khuwa\Cse_Project\coin_market_cap_top_50\Predicted_Price"
SENT_DIR = r"C:\Users\khuwa\Cse_Project\coin_market_cap_top_50\Market_Sentiment"

#FUNCTIONS
def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return None

def get_price(data, name, key="price_usd"):
    for entry in data:
        if entry["name"].lower() == name.lower():
            return float(entry.get(key, 0))
    return None

def get_sentiment(data, name):
    for entry in data:
        if entry["name"].lower() == name.lower():
            return int(entry.get("prediction", 0))
    return None

def classify_sentiment(p1, p2):
    if p1 == 0:
        return 0
    change = (p2 - p1) / p1
    if abs(change) <= 0.001:
        return 0
    return 1 if change > 0 else -1

#INITIALIZE CONFUSION COUNTERS
confusion = { -1: Counter(), 0: Counter(), 1: Counter() }

#LOOP THROUGH MARCH (03/01 to 03/30)
for day in range(1, 31):
    date_today = datetime.datetime.strptime(f"2025-03-{day:02d}", "%Y-%m-%d")
    date_tomorrow = date_today + datetime.timedelta(days=1)

    # Match raw file format: data_3_01_2025.json
    d1 = f"{date_today.month}_{date_today.day:02d}_{date_today.year}"
    d2 = date_tomorrow.strftime("%m_%d_%Y")

    raw_file = os.path.join(RAW_DIR, f"data_{d1}.json")
    pred_file = os.path.join(PRED_DIR, f"predicted_prices_{d2}.json")
    sent_file = os.path.join(SENT_DIR, f"market_sentiment_{d2}.json")

    raw_data = load_json(raw_file)
    pred_data = load_json(pred_file)
    sent_data = load_json(sent_file)

    if not raw_data or not pred_data or not sent_data:
        continue

    raw_map = {entry["name"].lower(): entry for entry in raw_data}
    pred_map = {entry["name"].lower(): entry for entry in pred_data}
    sent_map = {entry["name"].lower(): entry for entry in sent_data}

    for name in raw_map:
        if name in pred_map and name in sent_map:
            price_today = get_price(raw_data, name, "price_usd")
            price_predicted = get_price(pred_data, name, "predicted_price_usd")
            predicted_sentiment = get_sentiment(sent_data, name)

            if price_today is None or price_predicted is None or predicted_sentiment is None:
                continue

            actual_sentiment = classify_sentiment(price_today, price_predicted)

            if actual_sentiment == predicted_sentiment:
                confusion[actual_sentiment]["TP"] += 1
            else:
                confusion[actual_sentiment]["FN"] += 1
                confusion[predicted_sentiment]["FP"] += 1

            confusion[actual_sentiment]["Support"] += 1

#FINAL METRICS + VERIFICATION OUTPUT
metrics = {}
for cls in [-1, 0, 1]:
    TP = confusion[cls]["TP"]
    FP = confusion[cls]["FP"]
    FN = confusion[cls]["FN"]
    Support = confusion[cls]["Support"]

    # Print TP, FP, FN, Support for manual verification
    print(f"\nClass {cls}:")
    print(f"  TP = {TP}")
    print(f"  FP = {FP}")
    print(f"  FN = {FN}")
    print(f"  Support = {Support}")

    precision = TP / (TP + FP) if (TP + FP) else 0
    recall = TP / (TP + FN) if (TP + FN) else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0
    accuracy = TP / Support if Support else 0

    metrics[cls] = {
        "Precision": round(precision, 4),
        "Recall": round(recall, 4),
        "F1 Score": round(f1, 4),
        "Accuracy": round(accuracy, 4),
        "Support": Support
    }

#OUTPUT TABLE
df = pd.DataFrame.from_dict(metrics, orient="index")
df.index.name = "Sentiment Class"
print("\n=== Final Evaluation for March ===")
print(df)

#Save to CSV
df.to_csv("march_sentiment_evaluation.csv", index=True)
