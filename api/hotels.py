
import os
import requests
import datetime
from dotenv import load_dotenv

load_dotenv()


class HotelClient:

    def __init__(self):
        self.api_key = os.getenv("RAPIDAPI_KEY")
        self.headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "booking-com15.p.rapidapi.com"
        }

    def search(self, city_name: str, checkin_date: str, checkout_date: str, adults: int = 1, children: int = 0, limit: int = 7, currency: str = "INR") -> dict:
        try:
            print(f"🏨 [Hotel API] Searching for hotels in {city_name} from {checkin_date} to {checkout_date} for {adults} adults and {children} children...")
            dest_url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchDestination"
            dest_response = requests.get(dest_url, headers=self.headers, params={"query": city_name}, timeout=15)
            dest_data = dest_response.json()
            
            if not dest_data.get("data"):
                 return {"message": f"Sorry, the city '{city_name}' could not be found for hotel bookings."}
                
            dest_id = dest_data["data"][0].get("dest_id")
            search_type = dest_data["data"][0].get("search_type")
            
            if not dest_id:
                return {"message": f"Sorry, could not resolve destination ID for {city_name}."}

            hotel_url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchHotels"
            hotel_params = {
                "dest_id": dest_id,
                "search_type": search_type,
                "arrival_date": checkin_date,
                "departure_date": checkout_date,
                "adults": adults,
                "page_number": 1,
                "currency_code": currency,
            }
            
            if children > 0:
                hotel_params["children_number"] = children
                hotel_params["children_ages"] = ",".join(["7"] * children)  # Default age 7 for all children
            
            hotel_resp = requests.get(hotel_url, headers=self.headers, params=hotel_params, timeout=20)
            hotel_data = hotel_resp.json()
            
            results = []
            
            hotels_list = hotel_data.get("data", {}).get("hotels", [])
            
            if not hotels_list:
                return {"message": f"Sorry, no hotels were found in {city_name} for the selected dates."}
            
            for hotel_wrap in hotels_list[:limit]:
                hotel = hotel_wrap.get("property", {})
                
                price = "N/A"
                curr = currency
                price_breakdown = hotel.get("priceBreakdown", {})
                if price_breakdown:
                    gross = price_breakdown.get("grossPrice", {})
                    if gross:
                        price = gross.get("value", "N/A")
                        curr = gross.get("currency", currency)
                
                nights = 1
                try:
                    d1 = datetime.datetime.strptime(checkin_date, "%Y-%m-%d")
                    d2 = datetime.datetime.strptime(checkout_date, "%Y-%m-%d")
                    nights = max(1, (d2 - d1).days)
                except:
                    pass

                price_per_night = "N/A"
                if isinstance(price, (int, float)):
                    price_per_night = round(price / nights, 2)

                results.append({
                    "name": hotel.get("name", "Unknown Hotel"),
                    "reviewScore": hotel.get("reviewScore", "N/A"),
                    "reviewCount": hotel.get("reviewCount", 0),
                    "reviewScoreWord": hotel.get("reviewScoreWord", "N/A"),
                    "checkinDate": checkin_date,
                    "checkoutDate": checkout_date,
                    "checkin_time": hotel.get("checkin", {}).get("fromTime", "N/A"),
                    "checkout_time": hotel.get("checkout", {}).get("untilTime", "N/A"),
                    "price_per_night": price_per_night,
                    "currency": curr
                })
                
            return {
                "hotels": results
            }
            
        except Exception as e:
            print(f"❌ [Hotel API] Exception: {str(e)}")
            return {"error": str(e)}
