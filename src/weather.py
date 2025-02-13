class WeatherFormatter:
    @staticmethod
    def format_weather_data(data: dict) -> str:
        from datetime import datetime

        time_str = datetime.fromtimestamp(data['time_of_forecast']).strftime('%I:%M %p, %B %d, %Y')
        condition = data['weather_conditions'][0]['condition']
        description = data['weather_conditions'][0]['description']

        # get recommendations based on weather meeting report meeting various conditions
        advisory = WeatherFormatter._get_weather_advisory(data)
        clothing = WeatherFormatter._get_clothing_recommendation(data)

        weather_report_output = f"""
Weather Report for {data.get('city', 'Unknown')}
{'-' * 40}
Time: {time_str}
Temperature: {data['temperature']}°F
    High: {data['temperature_high']}°F
    Low: {data['temperature_low']}°F
Feels Like: {data['feels_like']}°F
Conditions: {condition} ({description})
Humidity: {data['humidity']}%
Wind Speed: {data['wind_speed']} mph

Recommendations:
{clothing}"""
        
        if advisory:
            weather_report_output += f"\n{advisory}"
        
        return weather_report_output
    
    @staticmethod
    def _get_weather_advisory(data: dict) -> str:
        temp = data['temperature']
        wind = data['wind_speed']
        conditions = data['weather_conditions'][0]['condition'].lower()

        if temp > 90:
            return "Heat Advisory: Stay hydrated and limit outdoor activity."
        elif temp < 32:
            return "Freeze Warning: Roads may be icy, please drive carefully."
        elif wind > 20:
            return "Wind Advisory: Hang on to your hats!"
        elif 'Rain' in conditions or 'Thunderstorm' in conditions:
            return "Rain Alert: Bring an umbrella."
        
        return ""  # no advisory
    
    @staticmethod
    def _get_clothing_recommendation(data: dict) -> str:
        """Get basic clothing recommendations based on temperature."""
        temp = data['temperature']
        conditions = data['weather_conditions'][0]['condition'].lower()

        if temp > 80:
            recommendation = "Wear light clothes and sunscreen if outside."
        elif temp > 65:
            recommendation = "Short sleeves should be fine. Shorts still OK."
        elif temp > 50:
            recommendation = "You'll want a light jacket."
        elif temp > 35:
            recommendation = "Coat and layers recommended."
        else:
            recommendation = "Winter gear is necessary! It's cold outside."

        # Add rain gear recommendation if needed
        if 'Rain' in conditions or 'Storm' in conditions:
            recommendation += "\nDon't forget your rain gear!"

        return recommendation