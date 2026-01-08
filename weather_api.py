import requests
import os
from dotenv import load_dotenv



load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

LOCATION = 'San Francisco,CA'
BASE_URL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'
UNIT_GROUP = 'metric'
CONTENT_TYPE = 'json'

base_url = f"{BASE_URL}{LOCATION}?unitGroup={UNIT_GROUP}&contentType={CONTENT_TYPE}&key={API_KEY}"




response = requests.get(base_url)

if response.status_code == 200:
    print("Data was retreived!")
    weather_data = response.json()

    if 'currentConditions' in weather_data:
        condition = weather_data['currentConditions']['conditions']
        print(condition)
    else:
        print("Current conditions data not found.")

    if 'currentConditions' in weather_data:
        condition = weather_data['currentConditions']['datetime']
        print(condition)
    else:
        print("Current conditions data not found.")
else:
    print(f"Failed to retreive data {response.status_code}")


