import http.client
import json
import re

# Perplexity API details
api_host = "api.perplexity.ai"
api_endpoint = "/chat/completions"
api_key = "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"

# Load cryptocurrency data from JSON file
input_file = "cryptocurrency_data.json"
output_file = "predictions.json"

with open(input_file, "r") as file:
    cryptocurrency_data = json.load(file)

# Prepare the prompt
prompt = (
    "Using the given cryptocurrency data, predict the prices and market caps for the next day. "
    "Provide the output as a JSON array with each cryptocurrency's name, predicted price, and predicted market cap. "
    "Do not provide anything but the JSON array. Also add a rank to each so i see that you have all 100 companies"
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
    "max_tokens": 2000,  # Adjust as needed
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

        # Convert the string to a JSON object
        predictions = json.loads(clean_content)

        # Save the cleaned JSON to a file
        with open(output_file, "w") as file:
            json.dump(predictions, file, indent=4)

        print(f"Predictions saved to {output_file}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    connection.close()