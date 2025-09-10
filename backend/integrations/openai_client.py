import os, requests, json

OPENAI_KEY = os.environ.get("OPENAI_API_KEY")

def generate_itinerary_with_prompt(system_prompt, user_prompt, model="gpt-4o-mini"):
    if not OPENAI_KEY:
        # fallback: return a canned response
        return "OpenAI key not provided. This is a demo itinerary: Day 1: Visit museum..."
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENAI_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": [
            {"role":"system","content": system_prompt},
            {"role":"user","content": user_prompt}
        ],
        "max_tokens": 800,
        "temperature": 0.7
    }
    r = requests.post(url, headers=headers, json=payload, timeout=20)
    if r.status_code==200:
        resp = r.json()
        try:
            return resp["choices"][0]["message"]["content"]
        except Exception:
            return json.dumps(resp)
    else:
        return f"OpenAI error: {r.status_code} {r.text}"
