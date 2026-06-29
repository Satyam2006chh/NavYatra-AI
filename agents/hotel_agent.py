
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from api.hotels import HotelClient
from prompts.templates import HOTEL_AGENT_SYSTEM_PROMPT
from agents.llm_utils import get_llm, invoke_with_retry
from dotenv import load_dotenv

load_dotenv()


@tool
def search_hotels(city_name: str, checkin_date: str, checkout_date: str, currency: str = "INR") -> str:
    """Search for hotels in a specific city on specific dates.

    Args:
        city_name: The city to search hotels in (e.g. Goa, Manali, Jaipur)
        checkin_date: Date in YYYY-MM-DD format
        checkout_date: Date in YYYY-MM-DD format
        currency: The currency code (e.g. INR, USD)

    Returns:
        JSON string with hotel names, prices, and review scores.
