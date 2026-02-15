"""
Flight API Client — Amadeus SDK
Dynamically searches flights based on user input.
"""

import os
from amadeus import Client, ResponseError
from dotenv import load_dotenv

load_dotenv()


class FlightClient:
    """Wrapper around Amadeus API for flight search."""

    def __init__(self):
        self.amadeus = Client(
            client_id=os.getenv("AMADEUS_CLIENT_ID"),
            client_secret=os.getenv("AMADEUS_CLIENT_SECRET"),
            hostname="test"
        )

    def search(self, origin_city: str, destination_city: str,
               departure_date: str, adults: int = 1, currency: str = "INR") -> dict:
        """Search flights between two cities."""
        try:
            origin_resp = self.amadeus.reference_data.locations.get(
                keyword=origin_city, subType="CITY"
            )
            dest_resp = self.amadeus.reference_data.locations.get(
                keyword=destination_city, subType="CITY"
            )

            if not origin_resp.data:
                return {
                    "no_flights": True,
                    "reason": f"no_airport_origin",
                    "message": (
                        f"The city '{origin_city}' does not have a recognized commercial airport "
                        f"in the Amadeus aviation database. This is common for smaller cities and towns. "
                        f"Consider traveling from the nearest major city with an airport, or "
                        f"use alternative transport like trains or buses to reach a nearby airport city."
                    )
                }
            if not dest_resp.data:
                return {
                    "no_flights": True,
                    "reason": "no_airport_destination",
                    "message": (
                        f"The city '{destination_city}' does not have a recognized commercial airport "
                        f"in the Amadeus aviation database. This is common for smaller cities and towns. "
                        f"Consider flying to the nearest major city with an airport and then using "
                        f"ground transport (train, bus, or cab) to reach {destination_city}."
                    )
                }

            origin_code = origin_resp.data[0].get("iataCode")
            dest_code = dest_resp.data[0].get("iataCode")

            if not origin_code:
                return {
                    "no_flights": True,
                    "reason": "no_iata_origin",
                    "message": (
                        f"'{origin_city}' was found but does not have an IATA airport code, "
                        f"meaning there is no commercial airport. Consider departing from "
                        f"the nearest major airport city."
                    )
                }
            if not dest_code:
                return {
                    "no_flights": True,
                    "reason": "no_iata_destination",
                    "message": (
                        f"'{destination_city}' was found but does not have an IATA airport code, "
                        f"meaning there is no commercial airport. Consider flying to the nearest "
                        f"major airport city and using ground transport to reach {destination_city}."
                    )
                }

            flight_resp = self.amadeus.shopping.flight_offers_search.get(
                originLocationCode=origin_code,
                destinationLocationCode=dest_code,
                departureDate=departure_date,
                adults=adults,
                currencyCode=currency
            )

            if not flight_resp.data:
                return {
                    "no_flights": True,
                    "reason": "no_flights_on_date",
                    "message": (
                        f"No flights were found from {origin_city} ({origin_code}) to "
                        f"{destination_city} ({dest_code}) on {departure_date}. "
                        f"This could be due to the route not being serviced on that date, "
                        f"or flights being sold out. Try checking nearby dates or "
                        f"alternative nearby airports."
                    )
                }

            flights = []
            for offer in flight_resp.data[:7]:
                itinerary = offer.get("itineraries", [{}])[0]
                segments = itinerary.get("segments", [])
                if not segments:
                    continue
                first = segments[0]
                last = segments[-1]
                flights.append({
                    "airline": first.get("carrierCode"),
                    "flight_number": first.get("number"),
                    "departure_airport": first.get("departure", {}).get("iataCode"),
                    "departure_time": first.get("departure", {}).get("at"),
                    "arrival_airport": last.get("arrival", {}).get("iataCode"),
                    "arrival_time": last.get("arrival", {}).get("at"),
                    "total_price": offer.get("price", {}).get("total"),
                    "currency": offer.get("price", {}).get("currency"),
                    "number_of_stops": len(segments) - 1
                })

            return {
                "origin_city": origin_city,
                "destination_city": destination_city,
                "origin_code": origin_code,
                "destination_code": dest_code,
                "departure_date": departure_date,
                "total_flights_returned": len(flights),
                "flights": flights
            }

        except ResponseError as error:
            return {
                "no_flights": True,
                "reason": "api_error",
                "message": f"Flight search encountered an error (Amadeus API: {error.response.status_code}). Please try again."
            }
        except Exception as e:
            return {
                "no_flights": True,
                "reason": "unknown_error",
                "message": f"An unexpected error occurred during flight search: {str(e)}"
            }
