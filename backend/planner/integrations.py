# integrations package to re-export clients
#from planner.integrations import weather_client, amadeus_client, openai_client
# backend/planner/integrations.py
# backend/planner/integrations.py
# backend/planner/integrations.py
from dotenv import load_dotenv
import os
from amadeus import Client as Amadeus
import openai
import requests

# Load environment variables from .env
load_dotenv()

print("DEBUG: OPENWEATHER_API_KEY =", os.getenv("OPENWEATHER_API_KEY"))

# ----------------------------
# Amadeus client
# ----------------------------
def get_amadeus_client():
    client_id = os.getenv("AMADEUS_API_KEY")
    client_secret = os.getenv("AMADEUS_API_SECRET")
    if not client_id or not client_secret:
        raise ValueError("Missing required Amadeus API credentials (AMADEUS_API_KEY / AMADEUS_API_SECRET)")
    return Amadeus(client_id=client_id, client_secret=client_secret)


# ----------------------------
# OpenAI client
# ----------------------------
from openai import OpenAI
import os

def openai_client(prompt: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("❌ Missing OPENAI_API_KEY in .env")

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are TripGenie, a smart travel planner."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content



# ----------------------------
# Weather client
# ----------------------------
def weather_client(city: str):
    api_key = os.getenv("OPENWEATHER_API_KEY")  # must match your .env
    if not api_key:
        raise ValueError("Missing OPENWEATHER_API_KEY in environment variables")
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        return {"error": f"Failed to fetch weather data: {str(e)}"}
