"""
Pydantic models for NavYatra AI.
Defines strict schemas for structured extraction and agent outputs.
"""

from pydantic import BaseModel, Field
from typing import Optional


class TravelQuery(BaseModel):
    """Structured travel query extracted from user's natural language input."""

    origin_city: str = Field(
        description="The city the traveler is departing from"
    )
    destination_city: str = Field(
        description="The city the traveler wants to visit"
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
    preferences: Optional[str] = Field(
        default=None,
        description="Special preferences: adventure, relaxation, food, culture, budget, luxury etc."
    )
