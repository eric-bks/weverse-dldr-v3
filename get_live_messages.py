import requests
import json
from urllib.parse import urlparse, parse_qs

# Function to fetch live chat messages
def fetch_live_chat(api_url, params, output_file):
	response = requests.get(api_url, params=params)
	if response.status_code == 200:
		chat_data = response.json()
		with open(output_file, 'w', encoding='utf-8') as f:
			json.dump(chat_data, f, ensure_ascii=False, indent=4)
		print(f"Chat data saved to {output_file}")
	else:
		print(f"Failed to fetch chat data. Status code: {response.status_code}")

# Input the URL
input_url = input("Enter the Weverse chat URL: ")

# Parse the input URL to extract the base URL and query parameters
parsed_url = urlparse(input_url)
api_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
params = parse_qs(parsed_url.query)

# Flatten the query parameters
params = {k: v[0] for k, v in params.items()}

# Define the output file name
output_file = "live_chat.json"

# Fetch live chat messages
fetch_live_chat(api_url, params, output_file)