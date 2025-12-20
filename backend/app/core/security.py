from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings

def create_token(data: dict, expires: timedelta) -> str:
    payload = data.copy()
    payload["exp"] = datetime.now() + expires
    return jwt.encode(
        # claims means the data to be encoded in the token
        claims=payload,
        key=settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )
