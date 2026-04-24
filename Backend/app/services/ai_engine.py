import os
import json
from datetime import date, timedelta

import google.generativeai as genai


def generate_itinerary(
    user_prefs: dict,
    dates: dict,
    group_size: int,
    budget_usd: float = None,
) -> list:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return _fallback_itinerary(dates)

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = _build_prompt(user_prefs, dates, group_size, budget_usd)

    try:
        response = model.generate_content(prompt)
        text = response.text
        start = text.find("[")
        end = text.rfind("]") + 1
        if start == -1 or end == 0:
            return _fallback_itinerary(dates)
        json_str = text[start:end]
        days = json.loads(json_str)
        return days
    except Exception:
        return _fallback_itinerary(dates)


def _build_prompt(
    user_prefs: dict,
    dates: dict,
    group_size: int,
    budget_usd: float = None,
) -> str:
    diet = user_prefs.get("diet", "mixed")
    interests = user_prefs.get("interests", ["culture", "food"])
    location_focus = user_prefs.get("location_focus", "Ubud, Seminyak, Kuta")
    date_from = dates.get("from", "")
    date_to = dates.get("to", "")
    budget_note = f"Total budget: USD {budget_usd}" if budget_usd else "No specific budget limit"

    interests_str = ", ".join(interests) if isinstance(interests, list) else str(interests)

    return f"""You are a Bali travel expert. Create a detailed day-by-day itinerary for a group trip to Bali.

Trip details:
- Travel dates: {date_from} to {date_to}
- Group size: {group_size} people
- Diet preference: {diet}
- Interests: {interests_str}
- Location focus: {location_focus}
- {budget_note}

Return ONLY a valid JSON array (no markdown, no explanation) where each element represents one day with this exact structure:
[
  {{
    "day": 1,
    "date": "YYYY-MM-DD",
    "activities": ["activity 1", "activity 2", "activity 3"],
    "meals": {{
      "breakfast": "meal description",
      "lunch": "meal description",
      "dinner": "meal description"
    }},
    "transport": "transport description for the day",
    "accommodation": "hotel/accommodation name and area",
    "estimated_cost_usd": 150.0
  }}
]

Make activities realistic for Bali. Use actual place names. Estimated cost per person per day. Start dates from {date_from}."""


def _fallback_itinerary(dates: dict) -> list:
    try:
        start = date.fromisoformat(dates.get("from", "2025-01-01"))
    except (ValueError, TypeError):
        start = date(2025, 1, 1)

    return [
        {
            "day": 1,
            "date": start.isoformat(),
            "activities": [
                "Arrive at Ngurah Rai International Airport",
                "Check in at hotel in Ubud",
                "Visit Tegallalang Rice Terraces",
                "Evening walk at Ubud Art Market",
            ],
            "meals": {
                "breakfast": "In-flight or hotel welcome breakfast",
                "lunch": "Warung Babi Guling Ibu Oka — local Balinese cuisine",
                "dinner": "Locavore Restaurant — farm-to-table Ubud dining",
            },
            "transport": "Private airport transfer to Ubud (approx 1.5 hrs)",
            "accommodation": "Komaneka at Bisma, Ubud",
            "estimated_cost_usd": 180.0,
        },
        {
            "day": 2,
            "date": (start + timedelta(days=1)).isoformat(),
            "activities": [
                "Morning visit to Sacred Monkey Forest Sanctuary",
                "Explore Ubud Royal Palace (Puri Saren Agung)",
                "Traditional Kecak Fire Dance at Uluwatu Temple",
                "Sunset at Tanah Lot Temple",
            ],
            "meals": {
                "breakfast": "Hotel breakfast with Balinese coffee",
                "lunch": "Sari Organik — organic vegetarian café in rice fields",
                "dinner": "Sundara Beach Club, Jimbaran — seafood BBQ on the beach",
            },
            "transport": "Private car hire for day trips around Ubud and south Bali",
            "accommodation": "Komaneka at Bisma, Ubud",
            "estimated_cost_usd": 160.0,
        },
        {
            "day": 3,
            "date": (start + timedelta(days=2)).isoformat(),
            "activities": [
                "Morning surf lesson at Kuta Beach",
                "Explore Seminyak boutique shops and galleries",
                "Spa treatment at Prana Spa Seminyak",
                "Sunset cocktails at Ku De Ta Beach Club",
            ],
            "meals": {
                "breakfast": "Revolver Espresso — specialty coffee and brunch",
                "lunch": "Nasi Ayam Kedewatan — traditional Balinese chicken rice",
                "dinner": "Merah Putih Restaurant — contemporary Indonesian fine dining",
            },
            "transport": "Private transfer from Ubud to Seminyak (approx 1 hr)",
            "accommodation": "The Layar Private Villas, Seminyak",
            "estimated_cost_usd": 200.0,
        },
    ]
