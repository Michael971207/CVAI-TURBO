import os
import time
from textwrap import dedent

# Gemini er valgfritt ved runtime:
# - Sett GEMINI_API_KEY i .env for å aktivere
# - Sett GEMINI_MODEL (default: gemini-2.0-flash)
# - Juster TEMPERATURE, TOP_P, TOP_K, MAX_OUTPUT_TOKENS via env

_GEMINI_AVAILABLE = True
try:
    import google.generativeai as genai
except Exception:
    _GEMINI_AVAILABLE = False

def _env_float(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, default))
    except Exception:
        return default

def _env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, default))
    except Exception:
        return default

def _build_prompt(name: str, cv_text: str, job_text: str, instructions: str) -> str:
    return dedent(f"""
    You are an expert career writing assistant. Write a concise, natural-sounding
    cover letter tailored for a student based on the CV and a job ad.

    HARD REQUIREMENTS:
    - 150–220 words.
    - Clear, human tone. No AI clichés.
    - Map 1–2 concrete matches between CV and job requirements.
    - End with a simple, confident call-to-action.
    - If instructions/style are provided, follow them but keep it professional.
    - Return only the letter text. No headings, no markdown.

    CANDIDATE:
    - Name: {name}

    CV (free text):
    ---
    {cv_text.strip()[:6000]}
    ---

    JOB (free text):
    ---
    {job_text.strip()[:6000]}
    ---

    EXTRA INSTRUCTIONS (optional):
    ---
    {instructions.strip()}
    ---
    """).strip()

def _stub_cover_letter(name: str, cv_text: str, job_text: str, instructions: str = "") -> str:
    base = f"""
    Dear Hiring Manager,

    I am excited to apply for this role. My background aligns strongly with the position:
    - Candidate: {name}
    - CV highlights: {cv_text[:200]}...
    - Job focus: {job_text[:200]}...

    {("Style/Tone: " + instructions) if instructions else ""}

    Thank you for your time.
    Best regards,
    {name}
    """
    return dedent(base).strip()

def generate_cover_letter(
    name: str,
    cv_text: str,
    job_text: str,
    instructions: str = "",
    model: str | None = None,
) -> str:
    """
    Primærfunksjon: generer søknadsbrev med Gemini.
    Faller tilbake til stub hvis API-nøkkel/pakke mangler eller kall feiler.
    """
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key or not _GEMINI_AVAILABLE:
        return _stub_cover_letter(name, cv_text, job_text, instructions)

    try:
        genai.configure(api_key=api_key)
        mdl = model or os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

        generation_config = {
            "temperature": _env_float("TEMPERATURE", 0.6),
            "top_p": _env_float("TOP_P", 0.95),
            "top_k": _env_int("TOP_K", 40),
            "max_output_tokens": _env_int("MAX_OUTPUT_TOKENS", 800),
        }

        # Safety settings kan justeres ved behov
        safety_settings = None

        prompt = _build_prompt(name, cv_text, job_text, instructions)
        gmodel = genai.GenerativeModel(model_name=mdl)

        # Enkel retry med backoff
        last_err = None
        for attempt in range(3):
            try:
                resp = gmodel.generate_content(
                    [prompt],
                    generation_config=generation_config,
                    safety_settings=safety_settings,
                )
                # Nyere SDK-er eksponerer .text
                if hasattr(resp, "text") and resp.text:
                    return resp.text.strip()
                # Fallback hvis output ligger i candidates
                if getattr(resp, "candidates", None):
                    for cand in resp.candidates:
                        parts = getattr(cand, "content", None) and getattr(cand.content, "parts", None)
                        if parts:
                            # slå sammen alle parts som tekst
                            joined = "".join(getattr(p, "text", "") or str(getattr(p, "inline_data", "")) for p in parts)
                            if joined.strip():
                                return joined.strip()
                # Hvis vi kom hit, prøv stub
                break
            except Exception as e:
                last_err = e
                time.sleep(0.6 * (attempt + 1))

        # Hvis alt feiler, returner stub
        return _stub_cover_letter(name, cv_text, job_text, f"{instructions}\n\n[Fallback: {type(last_err).__name__}]")

    except Exception as e:
        # Siste sikkerhetsnett
        return _stub_cover_letter(name, cv_text, job_text, f"{instructions}\n\n[Init error: {type(e).__name__}]")
