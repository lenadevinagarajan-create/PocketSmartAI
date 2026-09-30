# PocketSmart AI

A complete FastAPI + Jinja2 + SQLite + Gemini application based on the supplied PocketSmart AI project document.

## Features

- User registration/login with JWT bearer authentication
- Home Interior Budget Planner
- Party Budget Planner
- Jewelry Budget Planner with optional outfit image
- Gemini multimodal recommendation service
- Built-in fallback recommendations when Gemini is not configured or fails
- Recommendation history
- Responsive HTML/CSS/JavaScript UI
- Mock platform search links for Amazon, Flipkart, IKEA, Swiggy, Zomato and OYO
- OpenAPI/Swagger documentation at `/docs`

## Important implementation note

The source document names Gemini 1.5 Flash Pro and also mixes Flask/FastAPI. This implementation uses FastAPI consistently and reads `GEMINI_MODEL` from `.env`. This makes the project maintainable as Gemini models change.

The platform links are search links, not live marketplace APIs. Live prices, stock and availability are not claimed.

## Run

### Windows PowerShell

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
# edit .env and add GEMINI_API_KEY if you want Gemini
python -m uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
python -m uvicorn app.main:app --reload
```

## Test

```bash
pytest -q
```

Health check:
`GET /health`

Swagger:
`GET /docs`

## API routes

- `POST /api/register`
- `POST /api/login`
- `POST /api/logout`
- `POST /api/token`
- `GET /api/session-info`
- `GET /api/session-data`
- `GET /api/history`
- `GET /api/recommendations-details/{history_id}`
- `POST /api/generate-home`
- `POST /api/generate-party`
- `POST /api/generate-jewelry`

## Gemini

Set:

```env
GEMINI_API_KEY=your-key
GEMINI_MODEL=gemini-3.8-flash
```

The code uses Google's current `google-genai` Python SDK. The jewelry endpoint can send an uploaded JPG/PNG/WEBP image together with the text prompt.

If no key is supplied, the application still runs and uses the local demo catalog. This makes frontend/auth/database testing possible without an AI key.

## Project structure

```text
PocketSmartAI/
├── app/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   ├── templates/
│   ├── dependencies.py
│   └── main.py
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```
