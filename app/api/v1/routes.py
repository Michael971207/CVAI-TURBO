from fastapi import APIRouter
from app.api.v1.endpoints import auth, profile, cv, jobs, cover_letters, generate

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(profile.router, prefix="/profile", tags=["profile"])
api_router.include_router(cv.router, prefix="/cv", tags=["cv"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(cover_letters.router, prefix="/cover-letters", tags=["cover_letters"])
api_router.include_router(generate.router, prefix="/generate", tags=["generate"])
