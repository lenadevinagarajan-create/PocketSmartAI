from urllib.parse import quote_plus

def search_url(platform: str, query: str) -> str:
    q = quote_plus(query)
    urls = {
        "Amazon": f"https://www.amazon.in/s?k={q}",
        "Flipkart": f"https://www.flipkart.com/search?q={q}",
        "IKEA": f"https://www.ikea.com/in/en/search/?q={q}",
        "Swiggy": f"https://www.swiggy.com/search?query={q}",
        "Zomato": f"https://www.zomato.com/search?q={q}",
        "OYO": f"https://www.oyorooms.com/search?location={q}",
    }
    return urls.get(platform, f"https://www.google.com/search?q={q}")

def mock_catalog(planner: str, query: str, budget: float) -> list[dict]:
    data = {
        "home": [
            ("Warm LED ceiling light", "Lighting", 899, "Amazon"),
            ("Minimalist floor lamp", "Lighting", 1799, "IKEA"),
            ("Compact coffee table", "Furniture", 3499, "IKEA"),
            ("Decorative wall art set", "Decor", 1299, "Amazon"),
            ("Storage cabinet", "Storage", 4999, "Flipkart"),
            ("Cotton cushion set", "Decor", 999, "Amazon"),
        ],
        "party": [
            ("Veg catering package", "Food", 350, "Swiggy"),
            ("Birthday cake", "Food", 900, "Zomato"),
            ("Balloon decoration package", "Decoration", 1800, "Amazon"),
            ("Event chairs and tables", "Furniture", 2500, "Amazon"),
            ("Budget hotel rooms", "Accommodation", 2200, "OYO"),
        ],
        "jewelry": [
            ("Gold-tone jhumka earrings", "Earrings", 799, "Amazon"),
            ("Pearl necklace set", "Necklace", 1499, "Flipkart"),
            ("Minimal bracelet", "Bracelet", 599, "Amazon"),
            ("Kundan-style earrings", "Earrings", 1199, "Flipkart"),
            ("Elegant pendant set", "Necklace", 999, "Amazon"),
        ],
    }
    result = []
    for name, category, price, platform in data[planner]:
        if price <= budget * 0.75 or len(result) < 3:
            result.append({
                "name": name,
                "category": category,
                "estimated_price": float(price),
                "platform": platform,
                "reason": f"Fits the requested {query} context and is within a practical budget range.",
                "url": search_url(platform, name),
            })
    return result[:6]
