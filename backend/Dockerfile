# ---- Base image ----
# requires 3.12 or else slowapi code breaks
FROM python:3.12-slim

# ---- Work directory ----
WORKDIR /app

# ---- Copy application code --> always copy app files first then do pip install ----
COPY app app
COPY .env .env

# Clean Python cache
RUN find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
RUN find . -type f -name "*.pyc" -delete

# Install uv
RUN pip install --no-cache-dir uv
# ---- Install Python dependencies ----



COPY pyproject.toml ./
RUN uv pip install --system --no-cache .


# ---- Expose port ----
EXPOSE 8000

# ---- Run server ----
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
