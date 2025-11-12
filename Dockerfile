FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml /app/
RUN pip install --no-cache-dir uv && uv pip install -r <(uv pip compile pyproject.toml -q) || pip install fastapi uvicorn pydantic python-dotenv httpx
COPY app /app/app
ENV ENV=prod
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
