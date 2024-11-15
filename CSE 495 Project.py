import http.client
import json

connection = http.client.HTTPSConnection("pro-api.coinmarketcap.com")
api_key = "2ca92cfc-43ad-4ec6-9f43-353fb6bf7085"


headers = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": api_key
}

latest_endpoint = "/v1/cryptocurrency/listings/latest"
latest_parameters = "?start=1&limit=5&convert=USD"

connection.request("GET", latest_endpoint + latest_parameters, headers=headers)
latest_response = connection.getresponse()
latest_data = json.loads(latest_response.read().decode("utf-8"))

for currency in latest_data["data"]:
    name = currency["name"]
    rank = currency["cmc_rank"]
    current_price = currency["quote"]["USD"]["price"]
    percent_change_1h = currency["quote"]["USD"]["percent_change_1h"]
    percent_change_24h = currency["quote"]["USD"]["percent_change_24h"]
    percent_change_7d = currency["quote"]["USD"]["percent_change_7d"]

    #Fetch historical data
    symbol = currency["symbol"]
    historical_endpoint =  "/v1/cryptocurrency/category" #"/v2/cryptocurrency/ohlcv/historical"

    historical_parameters = f"?symbol={symbol}&time_start=2024-11-13&time_end=2024-11-13&interval=daily"

    connection.request("GET", historical_endpoint + historical_parameters, headers=headers)
    historical_response = connection.getresponse()
    historical_data = json.loads(historical_response.read().decode("utf-8"))

    # Extract starting (open) and (close) prices
    try:
        ohlcv_data = historical_data["data"]["quotes"][0]["quote"]["USD"]
        start_price = ohlcv_data["open"]
        end_price = ohlcv_data["close"]
        

        # Print the required information
        print(f"Name: {name}, Rank: {rank}")
        print(f"Percent Change (1h): {percent_change_1h:.2f}%")
        print(f"Percent Change (24h): {percent_change_24h:.2f}%")
        print(f"Percent Change (7d): {percent_change_7d:.2f}%\n")
        print(f"Starting Price: ${start_price:.2f}")
        print(f"End-of-Day Price: ${end_price:.2f}")
        print(f"Current Price: ${current_price:.2f}\n")
    except (KeyError, IndexError):
        print(f"Name: {name}, Rank: {rank}")
        print(f"Current Price: ${current_price:.2f}")
        print(f"Percent Change (1h): {percent_change_1h:.2f}%")
        print(f"Percent Change (24h): {percent_change_24h:.2f}%")
        print(f"Percent Change (7d): {percent_change_7d:.2f}%\n")
        print(f"Historical data not available for {name}. Please check the response format.\n")

# Note: Verify the historical data endpoint and response format in the CoinMarketCap documentation.
