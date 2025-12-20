from fastapi import APIRouter, Request, Response, HTTPException
from jose import jwt, JWTError
from datetime import timedelta

from .models import User
from app.core.password import hash_password, verify_password
from app.core.security import create_token
from app.core.cookies import set_auth_cookies, clear_auth_cookies
from app.core.csrf import validate_csrf
from app.core.limiter import limiter
from app.core.email_tokens import create_email_token, verify_email_token
from app.core.config import settings
from .email import send_verification_email
# from app.services.google_oauth import exchange_code_for_userinfo


from .schemas import LoginSchema, RegisterSchema, VerifyEmailRequest


# tags is used in swagger UI
router = APIRouter(prefix="/accounts", tags=["auth"])


# Register

@router.post("/register")
@limiter.limit("3/minute")
async def register(request: Request, data: RegisterSchema):
    # checking if user already exists
    if await User.find_one(User.email == data.email):
        raise HTTPException(400, "Email already exists")

    # creating user object
    user = User(
        name=data.name,
        email=data.email,
        hashed_password=hash_password(data.password),
        is_verified=False,
    )
    # inserting user in db
    await user.insert()

    token = create_email_token(str(user.id))
    send_verification_email(user.email, token)

    return {"message": "Verification email sent"}



@router.post("/verify-email")
async def verify_email(data: VerifyEmailRequest):
    user_id = verify_email_token(data.token)

    if not user_id:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired verification token"
        )

    user = await User.get(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.is_verified = True
    await user.save()

    return {"message": "Email verified successfully"}


# Login
@router.post("/login")
@limiter.limit("5/minute")
async def login(request: Request, data: LoginSchema, response: Response):
    user = await User.find_one(User.email == data.email)
    if not user or not user.hashed_password:
        raise HTTPException(401, "Invalid credentials")
    if not user.is_verified:
        raise HTTPException(403, "Email not verified")
    # password verification
    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")

    access = create_token({"sub": str(user.id)}, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh = create_token({"sub": str(user.id), "type": "refresh"}, timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))

    set_auth_cookies(response, access, refresh)
    return {"ok": True}

# Google login
# @router.post("/google")
# @limiter.limit("10/minute")
# async def google_login(request: Request, payload: dict, response: Response):
#     info = await exchange_code_for_userinfo(payload["code"])

#     user = await User.find_one(User.email == info["email"])
#     if not user:
#         user = User(email=info["email"], google_id=info["sub"], is_verified=True)
#         await user.insert()

#     access = create_token({"sub": str(user.id)}, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
#     refresh = create_token({"sub": str(user.id), "type": "refresh"}, timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))

#     set_auth_cookies(response, access, refresh)
#     return {"ok": True}

# Refresh Token
@router.post("/refresh")
@limiter.limit("30/minute")
async def refresh(request: Request, response: Response):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(401)

    try:
        payload = jwt.decode(token, settings.JWT_SECRET, [settings.JWT_ALGORITHM])
    except JWTError:
        raise HTTPException(401)

    access = create_token({"sub": payload["sub"]}, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    response.set_cookie("access_token", access, httponly=True, samesite="lax")
    return {"ok": True}

@router.post("/logout")
@limiter.limit("20/minute")
async def logout(request: Request, response: Response):
    validate_csrf(request)
    clear_auth_cookies(response)
    return {"ok": True}
