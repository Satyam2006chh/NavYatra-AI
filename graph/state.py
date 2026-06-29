
from typing import TypedDict, Optional


class TravelPlanState(TypedDict):

    user_query: str

    parsed_input: dict

    flight_results: str
    train_results: str
    hotel_results: str
    weather_results: str
    research_results: str

    raw_flight_results: dict
    raw_train_results: dict
    raw_hotel_results: dict
    raw_weather_results: dict
    raw_research_results: dict

    itinerary: str
