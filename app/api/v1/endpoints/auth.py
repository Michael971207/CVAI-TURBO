from fastapi import APIRouter, Header, HTTPException

router = APIRouter()

@router.get("/me")
def me(x_user_id: str | None = Header(default=None)):
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Missing x-user-id header (mock auth)")
    return {"user_id": x_user_id}
