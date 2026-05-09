import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")
url = "https://api.mistral.ai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}
payload = {
    "model": "mistral-large-latest",
    "messages": [
        {"role": "user", "content": "Hi"}
    ],
}

print(f"Testing Mistral API with key: {api_key[:5]}...")
try:
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {str(e)}")
