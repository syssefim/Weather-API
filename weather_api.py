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



try:
    response = requests.get(base_url, timeout=5, verify=True)
    response.raise_for_status() 

except requests.exceptions.HTTPError as errh:
    print(f"HTTP Error: {errh}")
except requests.exceptions.ReadTimeout as errrt:
    print("Timeout Error: The server took too long to respond.")
except requests.exceptions.ConnectionError as conerr:
    print("Connection Error: Check your internet or the URL.")
except requests.exceptions.RequestException as errex:
    print(f"General Error: {errex}")

else:
    print("Data was retrieved!")
    
    try:
        weather_data = response.json()
        
        if 'currentConditions' in weather_data:
            current_conditions = weather_data['currentConditions']
            
            condition_desc = current_conditions.get('conditions', 'Unknown')
            condition_time = current_conditions.get('datetime', 'Unknown')
            
            print(f"Condition: {condition_desc}")
            print(f"Time: {condition_time}")
        else:
            print("Current conditions data not found in response.")
            
    except ValueError:
        print("Error: content is not valid JSON")


