from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.api.v1.routes import api_router

load_dotenv()
app = FastAPI(title="CVAI Turbo API", version="0.1.0")

# CORS (tilpass origin senere)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # bytt til din frontend-origin senere
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"ok": True}

app.include_router(api_router, prefix="/api/v1")
