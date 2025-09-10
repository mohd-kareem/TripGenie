import datetime, math
POIS = [
    {"id":"poi_1","name":"Old Town Museum","category":"museum","lat":40.712,"lon":-74.006,"duration_mins":90,"opening":"09:00","closing":"17:00","popularity":0.9},
    {"id":"poi_2","name":"Riverside Park","category":"park","lat":40.715,"lon":-74.01,"duration_mins":60,"opening":"06:00","closing":"20:00","popularity":0.7},
    {"id":"poi_3","name":"City Cathedral","category":"historic","lat":40.713,"lon":-74.004,"duration_mins":45,"opening":"08:00","closing":"18:00","popularity":0.85},
    {"id":"poi_4","name":"Local Market","category":"food","lat":40.714,"lon":-74.005,"duration_mins":75,"opening":"07:00","closing":"15:00","popularity":0.8},
    {"id":"poi_5","name":"Modern Art Gallery","category":"museum","lat":40.716,"lon":-74.002,"duration_mins":80,"opening":"10:00","closing":"18:00","popularity":0.75},
    {"id":"poi_6","name":"Sunset Viewpoint","category":"scenic","lat":40.718,"lon":-74.008,"duration_mins":40,"opening":"00:00","closing":"23:59","popularity":0.7},
]

def score_poi(poi, prefs):
    cat_score = 1.0 if poi["category"] in prefs.get("categories",[]) else 0.5
    return poi["popularity"] * 0.6 + cat_score * 0.4

def generate_itinerary_demo(destination_name, start_date_str, nights, prefs, travelers=1):
    start_date = datetime.date.fromisoformat(start_date_str)
    plan = {"destination":destination_name,"start_date":start_date.isoformat(),"nights":nights,"days":[]}
    available = POIS.copy()
    for day in range(nights):
        day_date = start_date + datetime.timedelta(days=day)
        slots = [("09:00", "12:30"), ("13:30","17:00"), ("18:00","20:30")]
        items=[]
        for slot_start, slot_end in slots:
            best=None; best_score=-1
            for poi in available:
                s=score_poi(poi,prefs)
                if poi["opening"] <= slot_start and poi["closing"] >= slot_end:
                    if s>best_score:
                        best_score=s; best=poi
            if best:
                items.append({
                    "time":slot_start,
                    "poi":best["name"],
                    "category":best["category"],
                    "expected_duration_mins":best["duration_mins"]
                })
                available.remove(best)
        plan["days"].append({"date":day_date.isoformat(),"items":items})
    plan["notes"] = []
    if prefs.get("weather")=="rainy":
        plan["notes"].append("Weather looks rainy — pack an umbrella.")
    plan["estimated_budget_usd"] = nights * (50 if prefs.get("budget_level","medium")=="low" else (200 if prefs.get("budget_level")=="high" else 120))
    return plan
