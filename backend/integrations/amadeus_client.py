import os, requests, time

AMADEUS_KEY = os.environ.get("AMADEUS_API_KEY")
AMADEUS_SECRET = os.environ.get("AMADEUS_API_SECRET")
_AMADEUS_TOKEN = None
_AMADEUS_TOKEN_EXPIRES = 0

def _get_token():
    global _AMADEUS_TOKEN, _AMADEUS_TOKEN_EXPIRES, _AMADEUS_TOKEN
    if not AMADEUS_KEY or not AMADEUS_SECRET:
        return None
    if _AMADEUS_TOKEN and _AMADEUS_TOKEN_EXPIRES > time.time() + 30:
        return _AMADEUS_TOKEN
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    data = {"grant_type":"client_credentials", "client_id":AMADEUS_KEY, "client_secret":AMADEUS_SECRET}
    resp = requests.post(url, data=data, timeout=10)
    if resp.status_code==200:
        jd = resp.json()
        _AMADEUS_TOKEN = jd.get("access_token")
        _AMADEUS_TOKEN_EXPIRES = time.time() + jd.get("expires_in", 1800)
        return _AMADEUS_TOKEN
    else:
        return None

def search_flights(origin, destination, departure_date, adults=1):
    token = _get_token()
    if not token:
        # fallback stub
        return [{"provider":"DemoAir","flight_no":"DA123","dep":departure_date+"T08:00","arr":departure_date+"T12:00","price_usd":220}]
    headers = {"Authorization": f"Bearer {token}"}
    url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    params = {"originLocationCode": origin, "destinationLocationCode": destination, "departureDate": departure_date, "adults": adults, "max": 5}
    r = requests.get(url, headers=headers, params=params, timeout=10)
    if r.status_code==200:
        return r.json().get("data", [])
    else:
        return [{"error":"amadeus_error","status_code":r.status_code,"text":r.text}]
