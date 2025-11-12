from fastapi import APIRouter, Header, HTTPException
from app.schemas.profile import Profile, ProfileOut
from app.db.session import store

router = APIRouter()

def require_user(x_user_id: str | None):
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Missing x-user-id header")
    return x_user_id

@router.get("/", response_model=ProfileOut | None)
def get_profile(x_user_id: str | None = Header(default=None)):
    user_id = require_user(x_user_id)
    data = store["profiles"].get(user_id)
    if not data:
        return None
    return {"user_id": user_id, **data}

@router.post("/", response_model=ProfileOut)
def create_or_update_profile(payload: Profile, x_user_id: str | None = Header(default=None)):
    user_id = require_user(x_user_id)
    # enkel required-validering (frontend validerer også)
    for key in ["name","date_of_birth","gender","phone_number","address"]:
        if not getattr(payload, key):
            raise HTTPException(status_code=422, detail=f"Missing field: {key}")
    store["profiles"][user_id] = payload.model_dump()
    return {"user_id": user_id, **store["profiles"][user_id]}
