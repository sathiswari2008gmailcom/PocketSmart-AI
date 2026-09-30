from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config import get_settings
from .database import init_db
from .routes import pages,auth,planners
settings=get_settings()
@asynccontextmanager
async def lifespan(app): init_db(); settings.upload_dir.mkdir(exist_ok=True); yield
app=FastAPI(title=settings.app_name,version="1.0.0",lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=["http://127.0.0.1:8000","http://localhost:8000"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.mount("/static",StaticFiles(directory="static"),name="static"); app.mount("/uploads",StaticFiles(directory="uploads"),name="uploads")
app.include_router(pages.router); app.include_router(auth.router); app.include_router(planners.router)
@app.get("/health")
def health(): return {"status":"ok","gemini_configured":bool(settings.gemini_api_key)}
