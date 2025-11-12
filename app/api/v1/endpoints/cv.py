from fastapi import APIRouter, Header, HTTPException
from app.schemas.cv import CV, CVOut
from app.db.session import store

router = APIRouter()

def require_user(x_user_id: str | None):
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Missing x-user-id header")
    return x_user_id

@router.get("/", response_model=CVOut | None)
def get_cv(x_user_id: str | None = Header(default=None)):
    user_id = require_user(x_user_id)
    data = store["cvs"].get(user_id)
    if not data:
        return None
    return {"user_id": user_id, **data}

@router.post("/", response_model=CVOut)
def create_or_update_cv(payload: CV, x_user_id: str | None = Header(default=None)):
    user_id = require_user(x_user_id)
    # required-felt
    for key in ["education","work_experience","qualifications","language"]:
        if not getattr(payload, key):
            raise HTTPException(status_code=422, detail=f"Missing field: {key}")
    store["cvs"][user_id] = payload.model_dump()
    return {"user_id": user_id, **store["cvs"][user_id]}

@router.delete("/")
def delete_cv(x_user_id: str | None = Header(default=None)):
    user_id = require_user(x_user_id)
    store["cvs"].pop(user_id, None)
    return {"message": "CV deleted"}
