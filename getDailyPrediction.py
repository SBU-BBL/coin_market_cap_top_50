import os
import datetime
import http.client
import json
import re
from dotenv import load_dotenv

load_dotenv()


def fetch_and_save_data():
    """Fetches cryptocurrency data and saves it to a JSON file."""
    connection = http.client.HTTPSConnection("pro-api.coinmarketcap.com")
    api_key = os.getenv("COINMARKETCAP_API_KEY")

    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": api_key
    }

    latest_endpoint = "/v1/cryptocurrency/listings/latest"
    latest_parameters = "?start=1&limit=100&convert=USD"

    try:
        connection.request("GET", latest_endpoint + latest_parameters, headers=headers)
        latest_response = connection.getresponse()
        if latest_response.status != 200:
            raise Exception(f"Error fetching data: Status code {latest_response.status}")
        latest_data = json.loads(latest_response.read().decode("utf-8"))
    except Exception as e:
        print(f"An error occurred while fetching data: {e}")
        return None

    today_date = datetime.datetime.now().strftime("%m-%d-%Y")
    output_file = f"{today_date} data.json"

    results = []
    for currency in latest_data.get("data", []):
        try:
            name = currency["name"]
            symbol = currency["symbol"]
            rank = currency["cmc_rank"]
            current_price = currency["quote"]["USD"]["price"]
            market_cap = currency["quote"]["USD"]["market_cap"]
            percent_change_1h = currency["quote"]["USD"]["percent_change_1h"]
            percent_change_24h = currency["quote"]["USD"]["percent_change_24h"]
            percent_change_7d = currency["quote"]["USD"]["percent_change_7d"]
            volume_24h = currency["quote"]["USD"]["volume_24h"]

            results.append({
                "name": name,
                "symbol": symbol,
                "rank": rank,
                "market_cap_usd": market_cap,
                "price_usd": current_price,
                "percent_change_1h": percent_change_1h,
                "percent_change_24h": percent_change_24h,
                "percent_change_7d": percent_change_7d,
                "volume_24h_usd": volume_24h,
            })
        except KeyError as e:
            print(f"Missing data for a currency: {e}")

    with open(output_file, "w") as file:
        json.dump(results, file, indent=4)

    print(f"Saved data to {output_file}")
    return output_file


def call_ai_model(prompt, data, output_filename=None):
    """Calls the AI model with a given prompt. If output_filename is provided, saves result. Otherwise returns JSON."""
    api_host = "api.perplexity.ai"
    api_endpoint = "/chat/completions"
    api_key = os.getenv("PERPLEXITY_API_KEY")

    payload = {
        "model": "llama-3.1-sonar-small-128k-online",
        "messages": [
            {
                "role": "system",
                "content": "You are an AI model specialized in cryptocurrency market predictions."
            },
            {
                "role": "user",
                "content": f"Here is the cryptocurrency data: {json.dumps(data)}\n\n{prompt}"
            }
        ],
        "max_tokens": 10000,
        "temperature": 0.2,
        "top_p": 0.9,
        "stream": False
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        connection = http.client.HTTPSConnection(api_host)
        connection.request("POST", api_endpoint, body=json.dumps(payload), headers=headers)
        response = connection.getresponse()

        if response.status != 200:
            print(f"Error: Received status code {response.status}")
            print(f"Response: {response.read().decode('utf-8')}")
            return None

        content = json.loads(response.read().decode("utf-8"))["choices"][0]["message"]["content"]
        clean_content = re.sub(r"```json|```", "", content).strip()
        clean_content = re.sub(r"(['\w]+):", r'"\1":', clean_content)

        parsed_output = json.loads(clean_content)

        if output_filename:
            with open(output_filename, "w") as f:
                json.dump(parsed_output, f, indent=4)
            print(f"Saved predictions to {output_filename}")
        else:
            return parsed_output

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def generate_predictions(data_file):
    """Generates predictions using all 3 prompts."""
    today_date = datetime.datetime.now().strftime("%m-%d-%Y")
    tomorrow_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%m-%d-%Y")

    try:
        with open(data_file, "r") as file:
            crypto_data = json.load(file)
    except Exception as e:
        print(f"Error reading data file: {e}")
        return

    #Prompt 1: Price & Market Cap for 100 coins (split in memory)
    prompt1 = (
        "You are an AI model specialized in forecasting cryptocurrency prices and market caps for the next day.\n"
        "You are given today's data for 100 cryptocurrencies. Based on this data — and considering recent global events, regulations, and market patterns — forecast the expected values for tomorrow.\n\n"
        "For each cryptocurrency, provide your best estimate of the following:\n"
        "- name\n"
        "- rank\n"
        "- predicted_market_cap_usd\n"
        "- predicted_price_usd\n"
        "- percent_change_1h (expected)\n"
        "- percent_change_24h (expected)\n"
        "- percent_change_7d (expected)\n"
        "- volume_24h_usd (expected tomorrow)\n\n"
        "**Note:** Some values may coincidentally remain similar to today, but do not simply copy the input. Base each prediction on your understanding of current market dynamics.\n"
        "Return only a clean JSON array — no explanation or markdown formatting."
    )

    preds1 = call_ai_model(prompt1, crypto_data[:50])
    preds2 = call_ai_model(prompt1, crypto_data[50:])

    if preds1 and preds2:
        combined_preds = preds1 + preds2
        with open(f"{tomorrow_date} price_predictions.json", "w") as f:
            json.dump(combined_preds, f, indent=4)
        print(f"Combined price predictions saved to {tomorrow_date} price_predictions.json")
    else:
        print("❌ Failed to generate complete price predictions.")
        return

    #Prompt 2: Sentiment (1, 0, -1) based on price_predictions
    prompt2 = f"""
Simulate that today is {today_date}. You are a cryptocurrency forecasting AI operating on this date — not using any future or real-time information.

You are given today's market data for a list of cryptocurrencies. Each object includes:
- name
- symbol
- price_usd
- percent_change_1h
- percent_change_24h
- percent_change_7d
- market_cap_usd
- volume_24h_usd

Based *only* on this data — and your knowledge of market behavior, volatility patterns, and trading psychology up to and including {today_date} — estimate the short-term sentiment for each cryptocurrency over the next 24 hours.

For each cryptocurrency:
- If you believe the price will likely increase meaningfully, set "prediction" = 1 (bullish)
- If you believe the price will likely decrease meaningfully, set "prediction" = -1 (bearish)
- If you expect the price to remain relatively stable (within ±0.1%), set "prediction" = 0 (neutral)
- Assign a "confidence" score from 0 to 1, reflecting how confident you are in your sentiment prediction. Larger expected price movements should yield higher confidence scores.

Your output must be a JSON array structured as follows:
[
  {{
    "name": "<cryptocurrency_name>",
    "symbol": "<cryptocurrency_symbol>",
    "prediction": <prediction_value>,
    "confidence": <confidence_value>
  }},
  ...
]

Strict rules:
- Base your reasoning only on the provided data and your simulated understanding as of {today_date}
- Do NOT reference or use any future market data or hindsight knowledge
- Do NOT include price predictions, explanations, or any extra text
- Return ONLY one valid JSON array
"""

    call_ai_model(prompt2, combined_preds, f"{tomorrow_date} sentiment_predictions.json")

    #Prompt 3: Portfolio Recommendation
    prompt3 = (
    f"Today is the {today_date}. Pretend to be a cryptocurrency expert. Based on all the information you have up to today, "
    "create a theoretical portfolio from the cryptocurrency data that is designed to outperform the cryptocurrency index over the next day. "
    "Select exactly 10 cryptocurrencies from the provided data. "
    "Assign a weight (in %) to each selected coin so that the total adds up to exactly 100%. "
    "For each selected cryptocurrency, include the company name, ticker, weight, and sector. "
    "Your output must be in valid JSON format with no explanation or extra commentary — only return a JSON array in the following format:\n\n"
    "[{\"name\": \"Bitcoin\", \"ticker\": \"BTC\", \"weight\": 15.5, \"sector\": \"Store of Value\"}]"
    )

    call_ai_model(prompt3, crypto_data, f"{tomorrow_date} portfolio_recommendation.json")


def daily_task():
    """Runs the daily task of fetching data and generating predictions."""
    print("Running daily crypto prediction task...")
    data_file = fetch_and_save_data()
    if data_file:
        generate_predictions(data_file)


if __name__ == "__main__":
    daily_task()
