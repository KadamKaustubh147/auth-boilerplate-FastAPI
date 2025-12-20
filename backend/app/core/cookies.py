from fastapi import Response
from app.core.csrf import generate_csrf_token

def set_auth_cookies(response: Response, access: str, refresh: str):
    response.set_cookie(
        key="csrftoken",
        value=generate_csrf_token(),
        httponly=False,
        samesite="lax",
    )
    response.set_cookie(
        key="access_token",
        value=access,
        httponly=True,
        samesite="lax",
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh,
        httponly=True,
        samesite="lax",
        path="/accounts/refresh",
    )

def clear_auth_cookies(response: Response):
    response.delete_cookie("csrftoken")
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
