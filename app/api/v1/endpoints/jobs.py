from fastapi import APIRouter, Header, HTTPException
from app.schemas.job import JobApplication, Instructions

router = APIRouter()

def require_user(x_user_id: str | None):
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Missing x-user-id header")
    return x_user_id

@router.post("/new")
def new_job_application(job: JobApplication, instructions: Instructions | None = None, x_user_id: str | None = Header(default=None)):
    user_id = require_user(x_user_id)
    return {
        "user_id": user_id,
        "job": job.model_dump(),
        "instructions": (instructions.model_dump() if instructions else {"text": ""})
    }
