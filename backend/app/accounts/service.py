from fastapi import Request
from app.core.config import settings
from jose import jwt

def get_user_identifier(request: Request) -> str:
    try:
        # Read your JWT from cookies or headers
        token = request.cookies.get("access_token") or request.headers.get("Authorization")
        if token and token.startswith("Bearer "):
            token = token.split(" ", 1)[1]
        else:
            # but don't return IP
            return request.client.host  # fallback to IP if no user

        payload = jwt.decode(token, settings.JWT_SECRET, [settings.JWT_ALGORITHM])
        user_id = payload.get("sub")
        return f"user:{user_id}"
    except Exception:
        return request.client.host
