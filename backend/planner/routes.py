from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from planner.core import generate_itinerary_demo
from planner.integrations import weather_client, get_amadeus_client, openai_client

router = APIRouter()
@router.get("/demo")
async def demo_plan():
    return {"plan": "This is a demo itinerary."}

class ExtendedPlanReq(BaseModel):
    origin: Optional[str] = "NYC"
    destination: str = "SampleCity"
    start_date: str = "2025-09-20"
    nights: int = 3
    travelers: int = 1
    preferences: dict = {}

@router.post("/plan_extended")
async def plan_extended(req: ExtendedPlanReq):
    try:
        # 1) generate demo itinerary
        raw_itinerary = generate_itinerary_demo(
            req.destination, req.start_date, req.nights, req.preferences or {}, req.travelers
        )

        # Normalize into a list
        if isinstance(raw_itinerary, dict):
            itinerary = [{"day": k, "plan": v} for k, v in raw_itinerary.items()]
        elif isinstance(raw_itinerary, str):
            itinerary = [{"day": 1, "plan": raw_itinerary}]
        elif isinstance(raw_itinerary, list):
            itinerary = raw_itinerary
        else:
            itinerary = [{"day": 1, "plan": str(raw_itinerary)}]

        # 2) weather
        weather = weather_client(req.destination)

        # 3) flights
        amadeus = get_amadeus_client()
        flights_response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=req.origin,
            destinationLocationCode=req.destination,
            departureDate=req.start_date,
            adults=req.travelers
        )
        flights = getattr(flights_response, "data", flights_response)

        # 4) AI-enhanced itinerary
        ai_text = openai_client(f"Polish and expand this itinerary: {raw_itinerary}")

        return {
            "itinerary": itinerary,   # ✅ always a list
            "weather": weather,
            "flights": flights,
            "ai_text": ai_text
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))