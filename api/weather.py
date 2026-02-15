"""
Weather API Client — OpenWeatherMap API
Dynamically fetches current weather and forecast.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()


class WeatherClient:
    """Wrapper around OpenWeatherMap API for weather data."""

    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5"

    def search(self, city_name: str, units: str = "metric") -> dict:
        """Get current weather and 5-day forecast for a city."""
        try:
            # Current weather
            current_resp = requests.get(
                f"{self.base_url}/weather",
                params={"q": city_name, "appid": self.api_key, "units": units}
            )
            if current_resp.status_code != 200:
                return {"error": "Failed to fetch current weather", "details": current_resp.text}

            current = current_resp.json()

            # 5-day forecast
            forecast_resp = requests.get(
                f"{self.base_url}/forecast",
                params={"q": city_name, "appid": self.api_key, "units": units}
            )
            if forecast_resp.status_code != 200:
                return {"error": "Failed to fetch forecast", "details": forecast_resp.text}

            forecast = forecast_resp.json()

            result = {
                "city": current.get("name"),
                "country": current.get("sys", {}).get("country"),
                "current_weather": {
                    "temperature": current.get("main", {}).get("temp"),
                    "feels_like": current.get("main", {}).get("feels_like"),
                    "humidity": current.get("main", {}).get("humidity"),
                    "description": current.get("weather", [{}])[0].get("description"),
                    "wind_speed": current.get("wind", {}).get("speed")
                },
                "forecast": []
            }

            for item in forecast.get("list", [])[:8]:
                result["forecast"].append({
                    "datetime": item.get("dt_txt"),
                    "temperature": item.get("main", {}).get("temp"),
                    "description": item.get("weather", [{}])[0].get("description"),
                    "humidity": item.get("main", {}).get("humidity")
                })

            return result

        except Exception as e:
            return {"error": str(e)}
