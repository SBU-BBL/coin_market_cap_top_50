import os
import time
import datetime
import http.client
import json
import re


def fetch_and_save_data():
    connection = http.client.HTTPSConnection("pro-api.coinmarketcap.com")
    api_key = "2ca92cfc-43ad-4ec6-9f43-353fb6bf7085"

    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": api_key
    }

    latest_endpoint = "/v1/cryptocurrency/listings/latest"
    latest_parameters = "?start=1&limit=50&convert=USD"

    connection.request("GET", latest_endpoint + latest_parameters, headers=headers)
    latest_response = connection.getresponse()
    latest_data = json.loads(latest_response.read().decode("utf-8"))

   
    today_date = datetime.datetime.now().strftime("%m-%d-%Y")
    output_file = f"{today_date} data.json"

    results = []
    for currency in latest_data["data"]:
        name = currency["name"]
        rank = currency["cmc_rank"]
        current_price = currency["quote"]["USD"]["price"]
        market_cap = currency["quote"]["USD"]["market_cap"]

        results.append({
            "name": name,
            "rank": rank,
            "market_cap_usd": market_cap,
            "price_usd": current_price,
        })

 
    with open(output_file, "w") as file:
        json.dump(results, file, indent=4)

    print(f"Data saved to {output_file}")
    return output_file  


def generate_predictions(data_file):
    api_host = "api.perplexity.ai"
    api_endpoint = "/chat/completions"
    api_key = "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"

   
    tomorrow_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%m-%d-%Y")
    output_file = f"{tomorrow_date} prediction.json"


    with open(data_file, "r") as file:
        cryptocurrency_data = json.load(file)

    prompt = (
        "Do not provide anything but the JSON array, and ensure all 50 cryptocurrencies are included with ranks."
        "You are an AI model specialized in cryptocurrency market predictions"
        "Using the given cryptocurrency data and factoring in recent shifts in regulatory policies or announcements from major economies, predict the next day's price and market cap for each cryptocurrency." 
        "Provide the output as a JSON array with each cryptocurrency's name, rank, predicted market cap in USD, and predicted price in USD." 
        "Ensure your predictions reflect the potential influence of these regulatory changes on market sentiment and performance." 
        "Again provide nothing more than the JSON Array!"
    )

    payload = {
        "model": "llama-3.1-sonar-small-128k-online",
        "messages": [
            {
                "role": "system",
                "content": "You are an AI model specialized in cryptocurrency market predictions."
            },
            {
                "role": "user",
                "content": (
                    f"Here is the cryptocurrency data: {json.dumps(cryptocurrency_data)}\n\n"
                    + prompt
                )
            }
        ],
        "max_tokens": 3000,
        "temperature": 0.2,
        "top_p": 0.9,
        "stream": False
    }

    payload_json = json.dumps(payload)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        connection = http.client.HTTPSConnection(api_host)
        connection.request("POST", api_endpoint, body=payload_json, headers=headers)
        response = connection.getresponse()

        if response.status != 200:
            print(f"Error: Received status code {response.status}")
            print(f"Response: {response.read().decode('utf-8')}")
        else:
            response_data = response.read().decode("utf-8")
            response_json = json.loads(response_data)
            content = response_json["choices"][0]["message"]["content"]
            clean_content = re.sub(r"```json|```", "", content).strip()

           
            try:
                predictions = json.loads(clean_content)
                with open(output_file, "w") as file:
                    json.dump(predictions, file, indent=4)
                print(f"Predictions saved to {output_file}")
            except json.JSONDecodeError as e:
                print(f"Invalid JSON Content: {clean_content}")
                raise e

    except Exception as e:
        print(f"An error occurred: {e}")


def daily_task():
    print("Running daily task...")
    data_file = fetch_and_save_data() 
    generate_predictions(data_file)  

# Schedule the task
if __name__ == "__main__":
    while True:
        current_time = datetime.datetime.now()
        if current_time.hour == 23 and current_time.minute == 59:  # Check if it is 11:59 PM
            daily_task()
            time.sleep(60) 
        time.sleep(1)  
