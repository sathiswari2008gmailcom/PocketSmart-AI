# PocketSmart AI

A complete FastAPI + Jinja2 + SQLite GenAI budget recommendation application based on the supplied PocketSmart AI specification.

## Included
- Registration/login/logout + JWT cookie authentication
- Home Interior Planner
- Party Planner
- Jewelry Planner with optional image upload
- Gemini multimodal integration
- Structured JSON recommendations
- Recommendation history
- Amazon/Flipkart/IKEA/Swiggy/Zomato/OYO search destinations
- Local fallback engine when Gemini is not configured or fails
- Responsive frontend
- API docs at `/docs`
- Pytest tests

## VS Code / Windows
1. Open this folder in VS Code.
2. Install Python 3.11+.
3. In VS Code Terminal:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

If activation is blocked:
```powershell
Set-ExecutionPolicy -Scope Process Bypass
.venv\Scripts\Activate.ps1
```

4. Edit `.env` and set `GEMINI_API_KEY` if you want live Gemini generation. The app still runs without it using deterministic fallback recommendations.
5. Run:
```powershell
python run.py
```
6. Open `http://127.0.0.1:8000`.
7. API docs: `http://127.0.0.1:8000/docs`.

## Test
```powershell
pytest -q
```

## Main APIs
- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/auth/logout`
- `GET /api/auth/session-info`
- `POST /api/generate-home`
- `POST /api/generate-party`
- `POST /api/generate-jewelry`
- `GET /api/history`
- `GET /api/recommendations/{id}`
- `GET /api/session-data`
- `GET /health`

## Gemini model
The document specifies Gemini 1.5 Flash Pro. This implementation makes the model configurable through `GEMINI_MODEL` and defaults to `gemini-2.5-flash`; change the `.env` value if your available Gemini API model differs.

## Platform data
The source document calls for Amazon, Flipkart, IKEA, Swiggy, Zomato and OYO. This project deliberately does not fake private partner API access or live prices. It supplies search destinations and a local fallback catalog. Add authorized official/partner APIs later in `app/services/catalog.py` or a separate provider service.
