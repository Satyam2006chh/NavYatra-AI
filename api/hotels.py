"""
Hotel API Client — Geoapify Places API
Dynamically searches hotels based on city name.
Searches multiple accommodation categories for maximum results.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()


class HotelClient:
    """Wrapper around Geoapify API for hotel discovery."""

    def __init__(self):
        self.api_key = os.getenv("GEOAPIFY_API_KEY")

    def search(self, city_name: str, limit: int = 7) -> dict:
        """Search for hotels in a given city using broad accommodation categories."""
        try:
            # Step 1: Geocode city to coordinates
            geo_resp = requests.get(
                "https://api.geoapify.com/v1/geocode/search",
                params={"text": city_name, "apiKey": self.api_key}
            )
            geo_data = geo_resp.json()

            if not geo_data.get("features"):
                return {"error": f"City '{city_name}' not found"}

            coords = geo_data["features"][0]["geometry"]["coordinates"]
            lon, lat = coords[0], coords[1]

            # Step 2: Search all accommodation types using the parent category
            # Using "accommodation" returns hotels, resorts, guest houses, hostels etc.
            hotel_resp = requests.get(
                "https://api.geoapify.com/v2/places",
                params={
                    "categories": "accommodation",
                    "filter": f"circle:{lon},{lat},20000",
                    "limit": limit + 5,  # fetch extra to filter out unnamed ones
                    "apiKey": self.api_key
                }
            )
            hotel_data = hotel_resp.json()

            results = []
            seen_names = set()

            for place in hotel_data.get("features", []):
                props = place.get("properties", {})
                name = props.get("name", "")

                # Skip unnamed or duplicate hotels
                if not name or name in seen_names:
                    continue
                seen_names.add(name)

                results.append({
                    "hotel_name": name,
                    "address": props.get("formatted", "Address not available"),
                    "city": props.get("city", city_name),
                    "country": props.get("country", ""),
                    "category": props.get("categories", [""])[0].replace("accommodation.", "").title() if props.get("categories") else "Hotel",
                    "latitude": props.get("lat"),
                    "longitude": props.get("lon")
                })

                if len(results) >= limit:
                    break

            return {
                "city": city_name,
                "total_hotels_returned": len(results),
                "hotels": results
            }

        except Exception as e:
            return {"error": str(e)}
