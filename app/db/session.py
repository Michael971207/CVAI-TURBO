# Placeholder for future SQLAlchemy session.
# For now: in-memory stores so we can run without DB.
from typing import Dict, List
from datetime import datetime
import uuid

store = {
    "profiles": {},       # user_id -> profile dict
    "cvs": {},            # user_id -> cv dict
    "cover_letters": [],  # list of dicts
}

def new_id() -> str:
    return str(uuid.uuid4())

def now() -> datetime:
    return datetime.utcnow()
