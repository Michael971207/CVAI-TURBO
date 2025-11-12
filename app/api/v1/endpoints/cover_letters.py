from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from app.db.session import store, now

router = APIRouter()

def require_user(x_user_id: str | None):
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Missing x-user-id header")
    return x_user_id

class EditIn(BaseModel):
    instructions: str = ""
    text: str

@router.get("/")
def list_letters(x_user_id: str | None = Header(default=None)):
    user_id = require_user(x_user_id)
    items = [x for x in store["cover_letters"] if x["user_id"] == user_id]
    items = sorted(items, key=lambda x: x["created_at"], reverse=True)
    return {"items": items}

@router.put("/{cover_id}")
def edit_letter(cover_id: str, payload: EditIn, x_user_id: str | None = Header(default=None)):
    user_id = require_user(x_user_id)
    for x in store["cover_letters"]:
        if x["id"] == cover_id and x["user_id"] == user_id:
            x["text"] = payload.text
            x["edited_at"] = now()
            return x
    raise HTTPException(status_code=404, detail="Not found")

@router.delete("/{cover_id}")
def delete_saved(cover_id: str, x_user_id: str | None = Header(default=None)):
    user_id = require_user(x_user_id)
    before = len(store["cover_letters"])
    store["cover_letters"] = [x for x in store["cover_letters"] if not (x["id"] == cover_id and x["user_id"] == user_id)]
    return {"deleted": before - len(store["cover_letters"])}
