import requests

API_URL = "https://b002jdmi95.execute-api.ap-south-1.amazonaws.com/save"

data = {
    "username": "karan",
    "exercise": "Squat",
    "reps": 12,
    "score": 120
}

response = requests.post(API_URL, json=data)

print("Status:", response.status_code)
print("Response:", response.text)
