import os
from typing import Optional
from dotenv import load_dotenv

from .api import fetch_weather_data, WeatherAPIError
from .weather import WeatherFormatter

class WeatherCLI:

    def __init__(self):
        load_dotenv('.env.local')
        self.api_key = self._get_api_key()
        self.formatter = WeatherFormatter()
    
    def _get_api_key(self) -> Optional[str]:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            print("Error: OPENWEATHER_API_KEY not found in .env.local")
            return None
        return api_key
    
    def _prompt_for_location(self) -> dict:
        print("Welcome to command line weather app!")
        print("-----------------------------------")

        city = input("Enter city name: ").strip()
        while not city:
            print("City entry failed. Please try again.")
            city = input("Enter city name: ").strip()

        state = input("Enter state abbreviation (optional, press Enter to skip): ").strip().upper()
        if state:
            while len(state) != 2:
                print("State abbreviation should be exactly 2 characters (IN for Indiana, for example)")
                state = input("Enter state code: ").strip().upper()

        return {
            "city": city,
            "state": state if state else None,
            "country": "US"
        }
    
    def run(self):
        if not self.api_key:
            return
        
        try:
            location = self._prompt_for_location()
            print(f"\Collecting weather information for {location['city']}",
                  f", {location['state']}" if location['state'] else "",
                  "...")
            
            weather_data = fetch_weather_data(
                api_key=self.api_key,
                city=location['city'],
                state=location['state']
            )
            
            weather_data['city'] = location['city']
            
            formatted_weather = WeatherFormatter.format_weather_data(weather_data)
            print(formatted_weather)
        
        except WeatherAPIError as e:
            print(f"\nError: {str(e)}")