"""
Research API Client — Tavily Search API
Dynamically searches for tourist attractions and travel info.
"""

import os
from tavily import TavilyClient as TavilyAPI
from dotenv import load_dotenv

load_dotenv()


class ResearchClient:
    """Wrapper around Tavily API for travel research."""

    def __init__(self):
        self.client = TavilyAPI(api_key=os.getenv("TAVILY_API_KEY"))

    def search(self, query: str, max_results: int = 5) -> dict:
        """Search for travel-related information."""
        try:
            response = self.client.search(
                query=query,
                search_depth="advanced",
                max_results=max_results
            )

            if not response:
                return {"error": "No response from Tavily"}

            results = []
            for item in response.get("results", []):
                results.append({
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "content": item.get("content")
                })

            return {
                "query": query,
                "total_results": len(results),
                "results": results
            }

        except Exception as e:
            return {"error": str(e)}
