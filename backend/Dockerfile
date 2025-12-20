# ---- Base image ----
FROM python:3.13-slim



# ---- Work directory ----
WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv
# ---- Install Python dependencies ----
COPY pyproject.toml ./
RUN uv pip install --system --no-cache .

# ---- Copy application code ----
COPY app app
COPY .env .env

# ---- Expose port ----
EXPOSE 8000

# ---- Run server ----
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
