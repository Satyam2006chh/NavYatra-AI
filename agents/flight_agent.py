import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from api.flights import FlightClient
from prompts.templates import FLIGHT_AGENT_SYSTEM_PROMPT
from agents.llm_utils import get_llm, invoke_with_retry
from dotenv import load_dotenv

load_dotenv()


@tool
def search_flights(origin_city: str, destination_city: str,departure_date: str, adults: str = "1",currency: str = "INR") -> str:
    """Search for available flights between two cities on a specific date.
    Args:
        origin_city: The 3-letter IATA airport code for departure (e.g. DEL for Delhi, BOM for Mumbai)
        destination_city: The 3-letter IATA airport code for destination (e.g. GOI for Goa)
        departure_date: Date in YYYY-MM-DD format
        adults: Number of adult travelers as a string (e.g. "1", "2")
        currency: Currency code (INR, USD, EUR)
        Returns:
        JSON string with available flight options including airlines, times, and prices.
