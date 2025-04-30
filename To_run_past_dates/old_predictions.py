import os
import datetime
import http.client
import json
import re
import time

def call_ai_model(prompt, data, output_filename=None, retries=3, timeout=60):
    """Calls the AI model with a given prompt. Saves result to JSON file if output_filename is provided."""
    api_host = "api.perplexity.ai"
    api_endpoint = "/chat/completions"
    api_key = "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"

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

    for _ in range(retries):
        try:
            connection = http.client.HTTPSConnection(api_host, timeout=timeout)
            connection.request("POST", api_endpoint, body=json.dumps(payload), headers=headers)
            response = connection.getresponse()

            if response.status != 200:
                return None

            raw = response.read().decode("utf-8")
            content = json.loads(raw)["choices"][0]["message"]["content"]

            # Extract JSON array using regex
            match = re.search(r"\[\s*{.*?}\s*]", content, re.DOTALL)
            if not match:
                raise ValueError("Could not find a valid JSON array in the model output.")

            clean_json = match.group(0)
            parsed_output = json.loads(clean_json)

            if output_filename:
                os.makedirs(os.path.dirname(output_filename), exist_ok=True)
                with open(output_filename, "w") as f:
                    json.dump(parsed_output, f, indent=4)
            return parsed_output

        except Exception:
            time.sleep(5)

    return None


def generate_predictions_from_file(data_file_path, original_date_str):
    """Generates predictions from a specific raw data file."""
    try:
        with open(data_file_path, "r") as file:
            crypto_data = json.load(file)
    except:
        return

    input_date = datetime.datetime.strptime(original_date_str, "%m_%d_%Y")
    next_date_str = (input_date + datetime.timedelta(days=1)).strftime("%m_%d_%Y")

    #Prompt 1: Price & Market Cap
    prompt1 = (
        "You are an AI model specialized in forecasting cryptocurrency prices and market caps for the next day.\n"
        "You are given today's data for cryptocurrencies. Based on this data — and considering recent global events, regulations, and market patterns — forecast the expected values for tomorrow.\n\n"
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
        price_path = f"C:/Users/khuwa/Cse_Project/coin_market_cap_top_50/Predicted_Price/predicted_prices_{next_date_str}.json"
        with open(price_path, "w") as f:
            json.dump(combined_preds, f, indent=4)
        print(f"Saved {price_path}")
    else:
        return

    #Prompt 2: Independent Sentiment
    prompt2 = f"""
Simulate that today is {original_date_str}. You are a cryptocurrency forecasting AI operating on this date — not using any future or real-time information.

You are given today's market data for a list of cryptocurrencies. Each object includes:
- name
- symbol
- price_usd
- percent_change_1h
- percent_change_24h
- percent_change_7d
- market_cap_usd
- volume_24h_usd

Based *only* on this data — and your knowledge of market behavior, volatility patterns, and trading psychology up to and including {original_date_str} — estimate the short-term sentiment for each cryptocurrency over the next 24 hours.

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
- Base your reasoning only on the provided data and your simulated understanding as of {original_date_str}
- Do NOT reference or use any future market data or hindsight knowledge
- Do NOT include price predictions, explanations, or any extra text
- Return ONLY one valid JSON array
"""
    sentiment_path = f"C:/Users/khuwa/Cse_Project/coin_market_cap_top_50/Market_Sentiment/market_sentiment_{next_date_str}.json"
    call_ai_model(prompt2, crypto_data, sentiment_path)
    print(f"Saved {sentiment_path}")

    # --- Prompt 3: Portfolio Recommendation ---
    prompt3 = (
        f"Today is {original_date_str}. You are a cryptocurrency investment strategist.\n"
        "Your task is to build a short-term crypto portfolio expected to outperform the market over the next 24 hours.\n\n"
        "Instructions:\n"
        "- Select between 4 and 10 cryptocurrencies from the provided data.\n"
        "- Assign each a weight (in percent) representing how much of the portfolio it should occupy.\n"
        "- The sum of all weights must be **exactly 100.0** — no more, no less.\n"
        "- Keep track of the running total as you assign weights. Stop when you reach 100.0.\n"
        "- Do not guess or round arbitrarily. Use logical allocation.\n"
        "- If the weights do not sum to 100.0, your answer will be rejected.\n\n"
        "Your output must be a valid JSON array. Each entry must include:\n"
        "- name\n"
        "- ticker (symbol)\n"
        "- weight (float, in percent)\n"
        "- sector (e.g., 'AI', 'Smart Contracts', 'DeFi', etc.)\n\n"
        "Here is the correct format (but DO NOT copy the weights):\n"
        "[\n"
        "  {\"name\": \"Coin A\", \"ticker\": \"AAA\", \"weight\": <float>, \"sector\": \"Category\"},\n"
        "  {\"name\": \"Coin B\", \"ticker\": \"BBB\", \"weight\": <float>, \"sector\": \"Category\"},\n"
        "  ...\n"
        "]\n\n"
        "**Reminder:**\n"
        "- The total weight must be exactly 100.0\n"
        "- Output only the JSON array and nothing else"
    )

    portfolio_path = f"C:/Users/khuwa/Cse_Project/coin_market_cap_top_50/Portfolio/portfolio_{next_date_str}.json"
    call_ai_model(prompt3, crypto_data, portfolio_path)
    print(f"Saved {portfolio_path}")


if __name__ == "__main__":
    input_filename = "C:/Users/khuwa/Cse_Project/coin_market_cap_top_50/March Data/data_3_29_2025.json"
    original_date = "03_29_2025"  # month_day_year
    generate_predictions_from_file(input_filename, original_date)
 