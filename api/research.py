
import os
import requests
from dotenv import load_dotenv

load_dotenv()


class ResearchClient:

    def __init__(self):
        self.api_key = os.getenv("SERPAPI_KEY")

    def search(self, query: str, max_results: int = 7) -> dict:
        try:
            print(f"🗺️ [Research API] Searching for local attractions with query: '{query}'...")
            params = {
                "engine": "google_local",
                "q": query,
                "api_key": self.api_key
            }
            
            response = requests.get("https://serpapi.com/search.json", params=params, timeout=15)
            data = response.json()
            
            if "error" in data:
                return {"error": f"SerpApi Error: {data['error']}"}

            results = []
            local_results = data.get("local_results", [])
            for item in local_results[:max_results]:
                results.append({
                    "title": item.get("title", "Unknown"),
                    "rating": item.get("rating", "N/A"),
                    "reviews": item.get("reviews", "N/A"),
                    "type": item.get("type", "Tourist attraction"),
                    "address": item.get("address", "N/A"),
                    "hours": item.get("hours", "Check locally for timings"),
                    "description": item.get("description", "No description available.")
                })

            return {
                "query": query,
                "total_results": len(results),
                "attractions": results
            }

        except Exception as e:
            print(f"❌ [Research API] Exception: {str(e)}")
            return {"error": str(e)}
