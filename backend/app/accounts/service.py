from fastapi import Request
from app.core.config import settings
from jose import jwt, JWTError
from fastapi import HTTPException, status

from .models import User

# Learning --> never return none --> raise exceptions if not found
async def get_user(request: Request) -> User:
    token = request.cookies.get("access_token") or request.headers.get("Authorization")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    if token.startswith("Bearer "):
        token = token.split(" ", 1)[1]

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(401, "Invalid token")

        user = await User.get(user_id)

        if not user:
            raise HTTPException(401, "User not found")

        return user

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
# used for rate limiting
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
