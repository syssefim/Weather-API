import requests
import os
from dotenv import load_dotenv
import redis
import json
from datetime import date, time
from flask import Flask, render_template, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


#load weather api key from .env
load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

LOCATION = 'Kortum Trail, Jenner, CA 95450'
BASE_URL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'
UNIT_GROUP = 'metric'
CONTENT_TYPE = 'json'




# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

#Time to live value for redis cache
CACHE_TTL = 1800

#flask
app = Flask(__name__)
# Initialize Limiter with a key function (here, using the client's IP address)
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)








@app.route('/')
@limiter.limit("5 per minute")
def home():
    # Fetch weather data using caching
    cached_weather_data = fetch_weather_data(LOCATION)

    #print weather data if it exists
    if cached_weather_data:
        return f"The weather at {cached_weather_data['address'].split(',')[0]}\
            at {cached_weather_data['currentConditions']['datetime']}\
            is {cached_weather_data['currentConditions']['conditions'].lower()}"
    else:
        return 'Could not retreive weather data at this time...'
    


@app.route('/<city>')
def city(city):
    cached_weather_data = fetch_weather_data(city)

    if cached_weather_data:
        return f"The weather at {cached_weather_data['address'].split(',')[0]}\
            at {cached_weather_data['currentConditions']['datetime']}\
            is {cached_weather_data['currentConditions']['conditions'].lower()}"
    else:
        return 'Could not retreive weather data at this time...'

    #return render_template('city.html', content=city)











# Function to fetch weather data either from the cache or the external route
def fetch_weather_data(location):
    base_url = f"{BASE_URL}{location}?unitGroup={UNIT_GROUP}&contentType={CONTENT_TYPE}&key={API_KEY}"

    weather_data = r.get(location)

    if weather_data is None:
        try:
            # 1. Wrap the network call in a try/except block
            response = requests.get(base_url, timeout=10)
            
            # 2. Check for HTTP errors
            response.raise_for_status() 
            
            weather_data = response.json()
            
            # Store in cache
            r.set(location, json.dumps(weather_data), ex=CACHE_TTL)
            print("Data received from API...")
            
            return weather_data
            
        except requests.exceptions.RequestException as e:
            # This catches connection errors, timeouts, and HTTP errors
            print(f"Network error: {e}")
            return None
            
        except json.JSONDecodeError:
            print("Error parsing data from API")
            return None
    else:
        print('Data retreived from redis cache...')
        return json.loads(weather_data)






if __name__ == "__main__":
    app.run()
