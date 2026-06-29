"""
Pydantic models for NavYatra AI.
Defines strict schemas for structured extraction and agent outputs.
"""

from pydantic import BaseModel, Field
from typing import Optional, Any


class TravelQuery(BaseModel):
    """Structured travel query extracted from user's natural language input."""

    preferred_transport: str = Field(
        default="flight",
        description="User's preferred mode of transport: 'flight' or 'train'"
    )
    origin_city: str = Field(
        description="The city the traveler is departing from (e.g. Bangalore)"
    )
    destination_city: str = Field(
        description="The city the traveler wants to visit (e.g. Manali)"
    )
    origin_airport: str = Field(
        description="The 3-letter IATA airport code nearest to the origin city (e.g. BLR)"
    )
    destination_airport: str = Field(
        description="The 3-letter IATA airport code nearest to the destination city (e.g. KUU)"
    )
    origin_station_code: str = Field(
        description="The IRCTC railway station code nearest to the origin city (e.g. NDLS for Delhi)"
    )
    destination_station_code: str = Field(
        description="The IRCTC railway station code nearest to the destination city (e.g. CDG for Chandigarh)"
    )
    departure_date: str = Field(
        description="Departure date in YYYY-MM-DD format"
    )
    num_days: int = Field(
        default=3,
        description="Number of days for the trip"
    )
    adults: int = Field(
        default=1,
        description="Number of adult travelers"
    )
    currency: str = Field(
        default="INR",
        description="Preferred currency code like INR, USD, EUR"
    )
    preferences: Optional[Any] = Field(
        default=None,
        description="Special preferences: adventure, relaxation, food, culture, budget, luxury etc."
    )

