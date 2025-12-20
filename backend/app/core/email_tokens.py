from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings

def create_email_token(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "type": "email_verify",
        "exp": datetime.now() + timedelta(minutes=30),
    }
    return jwt.encode(payload, settings.JWT_SECRET, settings.JWT_ALGORITHM)

def verify_email_token(token: str) -> str:
    payload = jwt.decode(token, settings.JWT_SECRET, [settings.JWT_ALGORITHM])
    if payload.get("type") != "email_verify":
        raise ValueError("Invalid token type")
    return payload["sub"]
