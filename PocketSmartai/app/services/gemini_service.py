import json
from PIL import Image
from ..config import get_settings
from .recommendation_service import fallback_home,fallback_party,fallback_jewelry
settings=get_settings()
try:
    from google import genai
    from google.genai import types
except ImportError:
    genai=None; types=None

def client(): return genai.Client(api_key=settings.gemini_api_key) if genai and settings.gemini_api_key else None
def prompt(kind,d):
    return f'''You are PocketSmart AI, a budget planning assistant. Planner: {kind}. User data: {json.dumps(d,indent=2)}. Return ONLY valid JSON with keys planner_type, summary, budget, estimated_total, remaining_budget, allocation, items, source, disclaimer. Each item must contain title, category, estimated_price, quantity, platform, search_url, reason, notes. Keep the total within budget. Never claim prices are live or guaranteed. Platform names are discovery destinations unless verified data was supplied. estimated_total must equal sum(estimated_price * quantity).'''
def generate(kind,d,image=None):
    c=client()
    if not c: return fallback_home(d) if kind=="home" else fallback_party(d) if kind=="party" else fallback_jewelry(d)
    contents=[prompt(kind,d)]+([image] if image else [])
    try:
        r=c.models.generate_content(model=settings.gemini_model,contents=contents,config=types.GenerateContentConfig(response_mime_type="application/json"))
        out=json.loads(r.text or "{}"); out["source"]="gemini"; return out
    except Exception:
        return fallback_home(d) if kind=="home" else fallback_party(d) if kind=="party" else fallback_jewelry(d)
def generate_home(d): return generate("home",d)
def generate_party(d): return generate("party",d)
def generate_jewelry(d,image=None): return generate("jewelry",d,image)
