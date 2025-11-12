from pydantic import BaseModel

class CV(BaseModel):
    education: str
    work_experience: str
    qualifications: str
    language: str

class CVUpdate(CV):
    pass

class CVOut(CV):
    user_id: str
