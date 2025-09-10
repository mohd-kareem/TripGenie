import os, requests, datetime

OWM_KEY = os.environ.get("OPENWEATHER_API_KEY")

def geocode_city(city_name):
    # Use OpenWeatherMap geocoding
    if not OWM_KEY:
        return None
    url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {"q": city_name, "limit":1, "appid": OWM_KEY}
    r = requests.get(url, params=params, timeout=10)
    if r.status_code==200 and r.json():
        item = r.json()[0]
        return {"lat": item.get("lat"), "lon": item.get("lon")}
    return None

def get_weather_for_dates(city_name, start_date, nights):
    # returns list of daily forecasts. requires OWM_KEY
    if not OWM_KEY:
        # fallback: mock
        start = datetime.date.fromisoformat(start_date)
        out = []
        for i in range(nights):
            d = start + datetime.timedelta(days=i)
            out.append({"date": d.isoformat(), "summary":"Sunny (demo)", "temp_min_c":15+i, "temp_max_c":22+i})
        return out
    loc = geocode_city(city_name)
    if not loc:
        return []
    lat, lon = loc["lat"], loc["lon"]
    # call One Call 3.0 (or 2.5) to fetch daily forecasts
    url = "https://api.openweathermap.org/data/2.5/onecall"
    params = {"lat":lat, "lon":lon, "exclude":"minutely,hourly,alerts", "appid": OWM_KEY, "units":"metric"}
    r = requests.get(url, params=params, timeout=10)
    if r.status_code!=200:
        return []
    data = r.json()
    daily = data.get("daily", [])
    start = datetime.date.fromisoformat(start_date)
    out = []
    for i in range(nights):
        if i < len(daily):
            d = daily[i]
            day = datetime.date.fromtimestamp(d.get("dt")).isoformat()
            out.append({"date": day, "summary": d.get("weather",[{}])[0].get("description"), "temp_min_c": d.get("temp",{}).get("min"), "temp_max_c": d.get("temp",{}).get("max")})
        else:
            d = start + datetime.timedelta(days=i)
            out.append({"date": d.isoformat(), "summary":"No data", "temp_min_c": None, "temp_max_c": None})
    return out
