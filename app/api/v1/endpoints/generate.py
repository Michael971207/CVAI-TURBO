from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from app.db.session import store, new_id, now
from app.services.ai import generate_cover_letter

router = APIRouter()

def require_user(x_user_id: str | None):
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Missing x-user-id header")
    return x_user_id

class GenerateIn(BaseModel):
    instructions: str = ""
    job_application: str
    save: bool = False

@router.post("/", summary="Generate cover letter (optionally save)")
def generate_letter(payload: GenerateIn, x_user_id: str | None = Header(default=None)):
    user_id = require_user(x_user_id)
    profile = store["profiles"].get(user_id)
    cv = store["cvs"].get(user_id)

    if not profile or not cv:
        raise HTTPException(status_code=400, detail="Missing profile or CV. Please create those first.")

    name = profile.get("name", "Student")
    cv_text = "\n".join([
        cv.get("education",""),
        cv.get("work_experience",""),
        cv.get("qualifications",""),
        cv.get("language",""),
    ])
    job_text = payload.job_application

    letter = generate_cover_letter(name=name, cv_text=cv_text, job_text=job_text, instructions=payload.instructions)

    saved_id = None
    if payload.save:
        saved_id = new_id()
        store["cover_letters"].append({
            "id": saved_id,
            "user_id": user_id,
            "text": letter,
            "created_at": now(),
        })

    return {"cover_letter": letter, "saved_id": saved_id}

@router.get("/saved")
def list_saved(x_user_id: str | None = Header(default=None)):
    user_id = require_user(x_user_id)
    items = [x for x in store["cover_letters"] if x["user_id"] == user_id]
    items = sorted(items, key=lambda x: x["created_at"], reverse=True)
    return {"items": items}

@router.get("/{cover_id}")
def get_saved(cover_id: str, x_user_id: str | None = Header(default=None)):
    user_id = require_user(x_user_id)
    for x in store["cover_letters"]:
        if x["id"] == cover_id and x["user_id"] == user_id:
            return x
    raise HTTPException(status_code=404, detail="Not found")
