import os
import json
import pandas as pd

# Define folder paths
base_dir = "C:/Users/khuwa/Cse_Project/coin_market_cap_top_50"
folders = {
    "Raw_Data": os.path.join(base_dir, "March Data"),
    "Market_Sentiment": os.path.join(base_dir, "Market_Sentiment"),
    "Portfolio": os.path.join(base_dir, "Portfolio"),
    "Predicted_Prices": os.path.join(base_dir, "Predicted_Price"),
}

# Initialize storage for data
sheets_data = {
    "Raw Data": [],
    "Market Sentiment": [],
    "Portfolio": [],
    "Predicted Prices": []
}

# Helper function to load JSON files into a list of dicts, tagging each with the date
def load_jsons_from_folder(folder_path, sheet_key, date_pattern=r"(\d{1,2}_\d{1,2}_\d{4})"):
    for file in os.listdir(folder_path):
        if file.endswith(".json"):
            try:
                full_path = os.path.join(folder_path, file)
                with open(full_path, "r") as f:
                    data = json.load(f)

                # Extract date and normalize format
                match = re.search(date_pattern, file)
                date = match.group(1).replace("_", "-") if match else "unknown"

                if isinstance(data, list):
                    for entry in data:
                        entry["date"] = date
                        sheets_data[sheet_key].append(entry)
                elif isinstance(data, dict):
                    data["date"] = date
                    sheets_data[sheet_key].append(data)
            except Exception as e:
                print(f"Error reading {file}: {e}")

# Load all sheets
import re
load_jsons_from_folder(folders["Raw_Data"], "Raw Data")
load_jsons_from_folder(folders["Market_Sentiment"], "Market Sentiment")
load_jsons_from_folder(folders["Portfolio"], "Portfolio")
load_jsons_from_folder(folders["Predicted_Prices"], "Predicted Prices")

# Save to Excel
output_excel_path = os.path.join(base_dir, "clean_data.xlsx")
with pd.ExcelWriter(output_excel_path, engine='openpyxl') as writer:
    for sheet_name, data in sheets_data.items():
        df = pd.DataFrame(data)
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"✅ All JSON data compiled and saved to {output_excel_path}")
