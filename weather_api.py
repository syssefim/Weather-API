import requests
import os
from dotenv import load_dotenv
import redis
import json



load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

LOCATION = 'San Francisco,CA'
BASE_URL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'
UNIT_GROUP = 'metric'
CONTENT_TYPE = 'json'

base_url = f"{BASE_URL}{LOCATION}?unitGroup={UNIT_GROUP}&contentType={CONTENT_TYPE}&key={API_KEY}"







def main():
    

    cached_weather_data = fetch_weather_data(LOCATION)

    

    # Fetch user data directly from the external route
    response = requests.get(BASE_URL)
    external_weather_data = response.json()

    # Compare the data
    if cached_weather_data == external_weather_data:
        print("Data retrieved from cache matches data fetched from the external route.")
    else:
        print("Data mismatch: Cached data differs from data fetched from the external route.")









# Function to fetch weather data either from the cache or the external route
def fetch_weather_data(location):
    r = redis.Redis(host='localhost', port=6379, db=0)

    # Check if data is available in the cache
    weather_data = r.get(location)
    if weather_data is None:
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

                r.set(location, json.dumps(weather_data))
            else:
                print("Current conditions data not found in response.")
            
        except ValueError:
            print("Error: content is not valid JSON")        


    return weather_data




if __name__ == "__main__":
    main()














#notes
#possible guide to setting up redis for this project:
#https://www.geeksforgeeks.org/system-design/redis-cache/


