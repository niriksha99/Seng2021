import json
import requests

parameters = {"q": "chicken", "app_id": "111eb33b", "app_key": "672dc55881d4a63d132ab892bcf78fdf"}
response = requests.get("https://api.edamam.com/search", parameters)
print(response.status_code)

data = response.json()
print(data)
