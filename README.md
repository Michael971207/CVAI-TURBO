# CVAI Turbo (backend_fastapi) – Ready to Run at Home

## Run (home PC)
1) Install Python 3.12
2) `py -m venv .venv` + `.\.venv\Scripts\Activate.ps1`
3) `Copy-Item .\.env.example .\.env` (keys optional)
4) `py -m pip install --upgrade pip`
5) `py -m pip install fastapi uvicorn pydantic python-dotenv httpx`
6) `uvicorn app.main:app --reload` → http://127.0.0.1:8000

## Test
- `GET /health`
- `GET/POST /api/v1/profile` (requires header: x-user-id)
- `GET/POST/DELETE /api/v1/cv` (requires header)
- `POST /api/v1/generate` with body:
  { "instructions": "tone", "job_application": "plain text", "save": true }

## Next
- Swap AI stub with Gemini/OpenAI in app/services/ai.py
- Add Supabase + SQLAlchemy/Alembic
