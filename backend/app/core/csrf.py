import secrets
from fastapi import Request, HTTPException

CSRF_COOKIE_NAME = "csrftoken"
CSRF_HEADER_NAME = "X-CSRFToken"

def generate_csrf_token() -> str:
    return secrets.token_urlsafe(32)

# browser sends csrf token
# while axios adds X-CSRFToken header automatically from cookies

# when we have axios thing we can verify that it was not a CSRF, it was sent my our intended site

# so we have a simple code to validate csrf token

def validate_csrf(request: Request):
    cookie = request.cookies.get(CSRF_COOKIE_NAME)
    header = request.headers.get(CSRF_HEADER_NAME)

    if not cookie or not header or cookie != header:
        raise HTTPException(status_code=403, detail="CSRF failed")
