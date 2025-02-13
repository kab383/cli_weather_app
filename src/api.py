import requests
import os
from typing import Dict, Optional

class WeatherAPIError(Exception):
    pass

def fetch_weather_data(api_key: str, city: str,  state: str = None, country: str = "US", units: str = "imperial") -> Optional[Dict]:
    
    # determine whether or not user inputs are US based and set the location
    if state and country == "US":
        location = f"{city},{state},{country}"
    else:
        location = f"{city},{country}"

    base_url = os.getenv("BASE_URL")

    try:
        response = requests.get(
            base_url,
            params={
                "q": location,
                "appid": api_key,  # appid is required parameter naming convention per OpenWeather api documentation
                "units": units
            },
            timeout=10
        )

        # raise an error for bad HTTP codes
        response.raise_for_status()

        # returns as a dictionary as defined above, so we must use bracket notation in the return 
        data = response.json()  

        return {
            "time_of_forecast": data["dt"],
            "temperature": data["main"]["temp"],
            "temperature_low": data["main"]["temp_min"],
            "temperature_high": data["main"]["temp_max"],
            "feels_like": data["main"]["feels_like"],
            "weather_conditions": [
                {
                    "condition": w["main"],
                    "description": w["description"]
                }
                for w in data["weather"]  # list comprehension syntax
            ],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
        }
    except requests.exceptions.RequestException as e:
        # catch request errors
        raise WeatherAPIError(f"Error fetching weather data: {str(e)}")