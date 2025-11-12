from pydantic import BaseModel
import os

class Settings(BaseModel):
    ENV: str = os.getenv("ENV", "dev")
    ENABLE_SUPABASE: bool = os.getenv("ENABLE_SUPABASE", "false").lower() == "true"
    SUPABASE_URL: str | None = os.getenv("SUPABASE_URL")
    SUPABASE_ANON_KEY: str | None = os.getenv("SUPABASE_ANON_KEY")
    SUPABASE_SERVICE_ROLE_KEY: str | None = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")

settings = Settings()
