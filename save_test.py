import requests
import json

url = "https://b002jdmi95.execute-api.ap-south-1.amazonaws.com/save"

data = {
    "user_id": "karan1",
    "exercise": "Squat",
    "reps": 20,
    "score": 200
}

response = requests.post(url, json=data)

print("Status:", response.status_code)
print("Response:", response.text)
