import requests
import json


def get_weather(location):
    # First, geocode the location (city name or ZIP) to latitude and longitude
    # Using Open-Meteo's free geocoding API (no key required)
    geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1&language=en&format=json"

    try:
        geocode_response = requests.get(geocode_url)
        geocode_data = geocode_response.json()

        if 'results' not in geocode_data or len(geocode_data['results']) == 0:
            print(
                "Location not found. Please check the spelling or try a nearby city/ZIP code.")
            return

        lat = geocode_data['results'][0]['latitude']
        lon = geocode_data['results'][0]['longitude']
        city_name = geocode_data['results'][0]['name']
        country = geocode_data['results'][0].get('country', '')
        print(f"Weather for: {city_name}, {country}\n")

    except Exception as e:
        print("Error fetching location data:", e)
        return

    # Now fetch current weather using Open-Meteo API (free, no API key needed)
    weather_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "weather_code", "wind_speed_10m"],
        "temperature_unit": "celsius",   # Change to "fahrenheit" if you prefer
        "wind_speed_unit": "kmh",
        "timezone": "auto"
    }

    try:
        weather_response = requests.get(weather_url, params=params)
        weather_data = weather_response.json()

        current = weather_data['current']

        temp = current['temperature_2m']
        feels_like = current['apparent_temperature']
        humidity = current['relative_humidity_2m']
        wind_speed = current['wind_speed_10m']

        # Simple weather description based on WMO code
        code = current['weather_code']
        descriptions = {
            0: "Clear sky ☀️",
            1: "Mainly clear 🌤️",
            2: "Partly cloudy ⛅",
            3: "Overcast 🌥️",
            45: "Fog 🌫️",
            48: "Depositing rime fog 🌁",
            51: "Light drizzle 🌦️",
            53: "Moderate drizzle 🌧️",
            55: "Dense drizzle ☔",
            61: "Slight rain 🌧️",
            63: "Moderate rain 🌧️",
            65: "Heavy rain ⛈️",
            71: "Slight snow ❄️",
            73: "Moderate snow 🌨️",
            75: "Heavy snow ☃️",
            80: "Slight rain showers ☔",
            81: "Moderate rain showers 🌧️",
            82: "Violent rain showers ⛈️",
            95: "Thunderstorm ⚡"
        }
        condition = descriptions.get(code, "Unknown weather code")

        print(f"Temperature: {temp}°C")
        print(f"Feels like: {feels_like}°C")
        print(f"Humidity: {humidity}%")
        print(f"Wind speed: {wind_speed} km/h")
        print(f"Conditions: {condition}")

    except Exception as e:
        print("Error fetching weather data:", e)


# Main program
print("🌞 Simple Command-Line Weather App 🌞")

location = input("Enter a city name or ZIP code: ").strip()

if location:
    get_weather(location)
else:
    print("No location entered. Exiting.")
