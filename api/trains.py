
import os
import requests
import datetime
from dotenv import load_dotenv

load_dotenv()

class TrainClient:
    def __init__(self):
        self.api_key = os.getenv("RAPIDAPI_KEY")
        self.base_url = "https://irctc1.p.rapidapi.com/api/v3/trainBetweenStations"

    def search(self, origin_station_code: str, destination_station_code: str, start_date: str, num_days: int) -> dict:
        if not self.api_key:
            return {"error": "Missing RAPIDAPI_KEY for Train API"}

        if len(origin_station_code) < 3 or len(destination_station_code) < 3:
            return {"error": f"Invalid station codes: {origin_station_code} to {destination_station_code}"}

        headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "irctc1.p.rapidapi.com"
        }

        all_trains = []

        try:
            base_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            dates_to_search = [(base_date + datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(num_days + 1)]
            
            for date in dates_to_search:
                querystring = {
                    "fromStationCode": origin_station_code.upper(),
                    "toStationCode": destination_station_code.upper(),
                    "dateOfJourney": date
                }
                print(f"🚄 [Train API] Searching trains from {origin_station_code} to {destination_station_code} on {date}...")
                response = requests.get(self.base_url, headers=headers, params=querystring, timeout=20)
                
                if response.status_code == 200:
                    data = response.json()
                    trains = data.get("data", []) if "data" in data else data
                    if isinstance(trains, list):
                        for train in trains:
                            filtered_train = {
                                "train_name": train.get("train_name"),
                                "train_number": train.get("train_number"),
                                "from_station": train.get("from_station_name"),
                                "to_station": train.get("to_station_name"),
                                "from_std": train.get("from_std"),
                                "to_sta": train.get("to_sta"),
                                "run_days": train.get("run_days"),
                                "class_type": train.get("class_type"),
                                "has_pantry": train.get("has_pantry"),
                                "train_date": date
                            }
                            all_trains.append(filtered_train)
                else:
                    print(f"❌ [Train API] Failed on {date}: {response.status_code}")
                    
            if not all_trains:
                return {"message": "Sorry, no trains were found between these stations for the selected dates. Please check alternative routes or dates."}
                
            return {"trains": all_trains}

        except Exception as e:
            print(f"❌ [Train API] Exception: {str(e)}")
            return {"error": str(e)}
