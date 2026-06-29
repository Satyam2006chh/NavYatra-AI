
import os
import requests
import datetime
from dotenv import load_dotenv

load_dotenv()


class WeatherClient:

    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5"

    def search(self, city_name: str, start_date: str, num_days: int, units: str = "metric") -> dict:
        try:
            print(f"☁️ [Weather API] Fetching weather for {city_name} from {start_date} for {num_days} days...")
            current_resp = requests.get(
                f"{self.base_url}/weather",
                params={"q": city_name, "appid": self.api_key, "units": units},
                timeout=10
            )
            if current_resp.status_code != 200:
                return {"error": "Failed to fetch current weather", "details": current_resp.text}

            current = current_resp.json()

            forecast_resp = requests.get(
                f"{self.base_url}/forecast",
                params={"q": city_name, "appid": self.api_key, "units": units},
                timeout=15
            )
            if forecast_resp.status_code != 200:
                return {"error": "Failed to fetch forecast", "details": forecast_resp.text}

            forecast = forecast_resp.json()

            try:
                start_dt = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
                target_dates = [(start_dt + datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(num_days)]
            except:
                target_dates = []

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

            found_overlap = False
            for item in forecast.get("list", []):
                dt_txt = item.get("dt_txt", "")
                date_part = dt_txt.split(" ")[0] if dt_txt else ""
                
                if date_part in target_dates:
                    found_overlap = True
                    if "12:00:00" in dt_txt or not any(f["date"] == date_part for f in result["forecast"]):
                        if not any(f["date"] == date_part for f in result["forecast"]):
                            result["forecast"].append({
                                "date": date_part,
                                "time": dt_txt.split(" ")[1] if len(dt_txt.split(" ")) > 1 else "",
                                "temperature": item.get("main", {}).get("temp"),
                                "feels_like": item.get("main", {}).get("feels_like"),
                                "humidity": item.get("main", {}).get("humidity"),
                                "description": item.get("weather", [{}])[0].get("description"),
                                "wind_speed": item.get("wind", {}).get("speed"),
                                "chance_of_rain": item.get("pop", 0)
                            })
                            
            if not found_overlap and target_dates:
                result["note"] = f"Warning: The requested travel dates ({start_date} to {target_dates[-1]}) are beyond the 5-day forecast window. Providing the current 5-day forecast as a baseline. DO NOT pretend this is the forecast for their actual dates. Instead, analyze the seasonal climate typical for {city_name} during those dates."
                
                for item in forecast.get("list", []):
                    dt_txt = item.get("dt_txt", "")
                    date_part = dt_txt.split(" ")[0] if dt_txt else ""
                    if "12:00:00" in dt_txt or not any(f["date"] == date_part for f in result["forecast"]):
                        if not any(f["date"] == date_part for f in result["forecast"]):
                            result["forecast"].append({
                                "date": date_part,
                                "time": dt_txt.split(" ")[1] if len(dt_txt.split(" ")) > 1 else "",
                                "temperature": item.get("main", {}).get("temp"),
                                "feels_like": item.get("main", {}).get("feels_like"),
                                "humidity": item.get("main", {}).get("humidity"),
                                "description": item.get("weather", [{}])[0].get("description"),
                                "wind_speed": item.get("wind", {}).get("speed"),
                                "chance_of_rain": item.get("pop", 0)
                            })
                    if len(result["forecast"]) >= 5:
                        break

            return result

        except Exception as e:
            print(f"❌ [Weather API] Exception: {str(e)}")
            return {"error": str(e)}
