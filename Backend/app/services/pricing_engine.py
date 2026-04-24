RATE_CARDS = {
    "budget": {"hotel": 30, "food": 15, "transport": 10, "tours": 20},
    "mid":    {"hotel": 80, "food": 35, "transport": 25, "tours": 45},
    "premium": {"hotel": 200, "food": 80, "transport": 60, "tours": 100},
}


def calculate_price(days: int, group_size: int, price_tier: str) -> dict:
    rates = RATE_CARDS.get(price_tier, RATE_CARDS["mid"])
    return {
        "hotel": rates["hotel"] * days * group_size,
        "food": rates["food"] * days * group_size,
        "transport": rates["transport"] * days * group_size,
        "tours": rates["tours"] * days * group_size,
        "total": sum(v * days * group_size for v in rates.values()),
    }
