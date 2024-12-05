import http.client
import json
import re

# Perplexity API details
api_host = "api.perplexity.ai"
api_endpoint = "/chat/completions"
api_key = "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"

# Load cryptocurrency data from JSON file
input_file = "12-3-2024 data.json"
output_file = "12-4-2024 prediction.json"

with open(input_file, "r") as file:
    cryptocurrency_data = json.load(file)

# Prepare the prompt
prompt = (
    "Do not provide anything but the JSON array, and ensure all 50 cryptocurrencies are included with ranks."
    "You are an AI model specialized in cryptocurrency market predictions"
    "Using the given cryptocurrency data and factoring in recent shifts in regulatory policies or announcements from major economies, predict the next day's price and market cap for each cryptocurrency." 
    "Provide the output as a JSON array with each cryptocurrency's name, rank, predicted market cap in USD, and predicted price in USD." 
    "Ensure your predictions reflect the potential influence of these regulatory changes on market sentiment and performance." 
    "Again provide nothsing more than the JSON Array!"
)

# Prepare the payload for the Perplexity API
payload = {
    "model": "llama-3.1-sonar-small-128k-online",  # Replace with your desired model
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
    "max_tokens": 3000,  # Adjust as needed
    "temperature": 0.2,
    "top_p": 0.9,
    "stream": False
}

# Convert payload to JSON string
payload_json = json.dumps(payload)

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

try:
    connection = http.client.HTTPSConnection(api_host)
    
    # Prepare headers
    formatted_headers = {key: value for key, value in headers.items()}

    # Send POST request
    connection.request("POST", api_endpoint, body=payload_json, headers=formatted_headers)
    response = connection.getresponse()
    
    # Check the status code
    if response.status != 200:
        print(f"Error: Received status code {response.status}")
        print(f"Response: {response.read().decode('utf-8')}")
    else:
        # Parse the response
        response_data = response.read().decode("utf-8")
        response_json = json.loads(response_data)

        # Extract and clean the "content" field
        content = response_json["choices"][0]["message"]["content"]

        # Remove the ```json markers and clean up the string
        clean_content = re.sub(r"```json|```", "", content).strip()

        # Debugging: Validate JSON manually if needed
        try:
            predictions = json.loads(clean_content)
        except json.JSONDecodeError as e:
            print(f"Invalid JSON Content: {clean_content}")
            raise e

        # Save the cleaned JSON to a file
        with open(output_file, "w") as file:
            json.dump(predictions, file, indent=4)

        print(f"Predictions saved to {output_file}")

except Exception as e:
    print(f"An error occurred: {e}")
