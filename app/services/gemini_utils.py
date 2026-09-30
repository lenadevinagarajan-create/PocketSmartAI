import json
import re
from typing import Any
from app.core.config import settings
from app.services.catalog import mock_catalog

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None

SYSTEM_PROMPT = """You are PocketSmart AI, a budget-aware recommendation assistant.
Return ONLY valid JSON matching this shape:
{
  "summary": "short explanation",
  "allocations": {"category": 0},
  "recommendations": [
    {
      "name": "item",
      "category": "category",
      "estimated_price": 0,
      "platform": "Amazon|Flipkart|IKEA|Swiggy|Zomato|OYO",
      "reason": "why it fits"
    }
  ]
}
Never claim live inventory or live prices. Estimated prices must be clearly treated as estimates.
Keep total estimated recommendation cost within the user's budget. Prefer practical, diverse suggestions.
"""

def _extract_json(text: str) -> dict[str, Any] | None:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, flags=re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                return None
    return None

def _normalise(data: dict, planner: str, budget: float, query: str) -> dict:
    recs = []
    running = 0.0
    allowed = {"Amazon", "Flipkart", "IKEA", "Swiggy", "Zomato", "OYO"}
    for item in data.get("recommendations", [])[:8]:
        try:
            price = float(item.get("estimated_price", 0))
        except (ValueError, TypeError):
            continue
        if price <= 0 or running + price > budget:
            continue
        platform = item.get("platform", "Amazon")
        if platform not in allowed:
            platform = "Amazon"
        recs.append({
            "name": str(item.get("name", "Suggested item"))[:160],
            "category": str(item.get("category", "General"))[:80],
            "estimated_price": price,
            "platform": platform,
            "reason": str(item.get("reason", "Fits the selected requirements."))[:500],
            "url": __import__("app.services.catalog", fromlist=["search_url"]).search_url(platform, str(item.get("name", query))),
        })
        running += price

    if not recs:
        recs = mock_catalog(planner, query, budget)
        running = sum(x["estimated_price"] for x in recs)

    return {
        "summary": str(data.get("summary", "Recommendations prepared within the requested budget."))[:1000],
        "allocations": {str(k): float(v) for k, v in (data.get("allocations") or {}).items() if isinstance(v, (int, float))},
        "recommendations": recs,
        "budget_used": round(running, 2),
    }

def generate_recommendations(planner: str, payload: dict, image_bytes: bytes | None = None, image_mime: str | None = None) -> dict:
    budget = float(payload["budget"])
    query = json.dumps(payload, ensure_ascii=False)

    if not settings.gemini_api_key or genai is None:
        return {
            **_normalise({}, planner, budget, query),
            "source": "fallback",
            "warning": "Gemini API is not configured. Showing built-in demo recommendations.",
        }

    try:
        client = genai.Client(api_key=settings.gemini_api_key)
        prompt = f"{SYSTEM_PROMPT}\nPlanner: {planner}\nUser input JSON: {query}"
        contents = [prompt]
        if image_bytes and image_mime:
            contents.append(types.Part.from_bytes(data=image_bytes, mime_type=image_mime))

        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=contents,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.3,
                max_output_tokens=1800,
            ),
        )
        parsed = _extract_json(response.text or "")
        if not parsed:
            raise ValueError("Gemini returned invalid JSON")
        return {
            **_normalise(parsed, planner, budget, query),
            "source": f"gemini:{settings.gemini_model}",
            "warning": None,
        }
    except Exception as exc:
        fallback = _normalise({}, planner, budget, query)
        fallback["source"] = "fallback"
        fallback["warning"] = f"Gemini request failed, so demo recommendations were used: {type(exc).__name__}"
        return fallback
