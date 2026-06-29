
import os
import requests
import datetime
from dotenv import load_dotenv

load_dotenv()


class FlightClient:

    def __init__(self):
        self.api_key = os.getenv("SERPAPI_KEY")

    def search(self, origin_city: str, destination_city: str,
               start_date: str, num_days: int = 1, adults: int = 1, currency: str = "INR") -> dict:
        try:
            all_extracted_flights = []
            
            base_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            dates_to_search = [(base_date + datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(num_days + 1)]
            
            for date in dates_to_search:
                if len(all_extracted_flights) >= 8:
                    break
                    
                params = {
                    "engine": "google_flights",
                    "departure_id": origin_city,
                    "arrival_id": destination_city,
                    "outbound_date": date,
                    "adults": adults,
                    "currency": currency,
                    "type": "2",
                    "api_key": self.api_key
                }
                
                print(f"✈️ [Flight API] Searching flights from {origin_city} to {destination_city} on {date}...")
                response = requests.get("https://serpapi.com/search.json", params=params, timeout=20)
                data = response.json()
                
                if "error" in data:
                    print(f"❌ [Flight API] Failed on {date}: {data['error']}")
                    continue
                    
                best_flights = data.get("best_flights", [])
                other_flights = data.get("other_flights", [])
                all_flights = best_flights + other_flights
                
                for flight in all_flights:
                    if len(all_extracted_flights) >= 8:
                        break
                        
                    flights_list = flight.get("flights", [])
                    if not flights_list:
                        continue
                        
                    flight_legs = []
                    for leg in flights_list:
                        flight_legs.append({
                            "airline": leg.get("airline"),
                            "flight_number": leg.get("flight_number"),
                            "airplane": leg.get("airplane"),
                            "travel_class": leg.get("travel_class"),
                            "departure_airport": {
                                "name": leg.get("departure_airport", {}).get("name"),
                                "id": leg.get("departure_airport", {}).get("id"),
                                "time": leg.get("departure_airport", {}).get("time")
                            },
                            "arrival_airport": {
                                "name": leg.get("arrival_airport", {}).get("name"),
                                "id": leg.get("arrival_airport", {}).get("id"),
                                "time": leg.get("arrival_airport", {}).get("time")
                            },
                            "duration": leg.get("duration")
                        })
                        
                    all_extracted_flights.append({
                        "total_price": flight.get("price", "N/A"),
                        "currency": currency,
                        "type": flight.get("type"),
                        "legs": flight_legs
                    })
                    
            if not all_extracted_flights:
                 return {
                    "message": f"Sorry, no flights were found from {origin_city} to {destination_city} for the selected dates. Please check alternative routes or dates."
                }
                
            return {
                "flights": all_extracted_flights
            }
            
        except Exception as e:
            print(f"❌ [Flight API] Exception: {str(e)}")
            return {"error": str(e)}
