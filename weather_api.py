import requests

API_KEY = '8VXW7UBZSDUMZN8NW569D55XP'
LOCATION = 'San Francisco,CA'
BASE_URL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'
UNIT_GROUP = 'metric'
CONTENT_TYPE = 'json'

base_url = f"{BASE_URL}{LOCATION}?unitGroup={UNIT_GROUP}&contentType={CONTENT_TYPE}&key={API_KEY}"




response = requests.get(base_url)

if response.status_code == 200:
    print("Data was retreived!")
    weather_data = response.json()
    print(weather_data)
else:
    print(f"Failed to retreive data {response.status_code}")


