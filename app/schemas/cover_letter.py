from pydantic import BaseModel
from datetime import datetime

class CoverLetter(BaseModel):
    text: str

class CoverLetterOut(CoverLetter):
    id: str
    user_id: str
    created_at: datetime
