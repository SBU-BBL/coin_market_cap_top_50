import requests

# API URL and key
url = "https://your-api-url.com/content/*"  # Replace with your actual API URL
api_key = "2ca92cfc-43ad-4ec6-9f43-353fb6bf7085"  # Your actual API key

# Headers for authorization
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Send a GET request to fetch data from the API
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()  # Parse JSON response
    print("Data received:", data)
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")