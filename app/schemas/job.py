from pydantic import BaseModel

class JobApplication(BaseModel):
    job_title: str
    job_description: str
    job_qualifications: str

class Instructions(BaseModel):
    text: str = ""  # style/tone free text
