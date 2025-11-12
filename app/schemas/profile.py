from pydantic import BaseModel, Field

class Profile(BaseModel):
    name: str
    date_of_birth: str  # mm/dd/yy
    gender: str  # female/male/other
    phone_number: str
    address: str

class ProfileUpdate(Profile):
    pass

class ProfileOut(Profile):
    user_id: str = Field(..., description="User UUID")
