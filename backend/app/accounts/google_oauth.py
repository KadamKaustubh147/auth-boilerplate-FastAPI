from typing import Optional
from fastapi import Request, HTTPException
from authlib.integrations.starlette_client import OAuth
from app.core.config import settings

oauth = OAuth()

# Register the Google OAuth client
oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile",
        # For offline access (refresh token), include prompt=consent when redirecting login
    },
)


async def get_google_authorize_url(request: Request) -> str:
    """
    Get the Google authorization URL to redirect users to.

    The frontend should redirect users to this URL so they can authenticate with Google.
    """
    redirect_uri = settings.GOOGLE_REDIRECT_URI
    return await oauth.google.authorize_redirect(request, redirect_uri)


async def exchange_code_for_tokens(request: Request):
    """
    After Google redirects back with a code, exchange it for access + refresh tokens.
    """
    try:
        # This returns the token dict:
        # { "access_token": "...", "id_token": "...", "expires_in": ..., "refresh_token": "...", ... }
        token = await oauth.google.authorize_access_token(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to get tokens: {e}")

    if "access_token" not in token:
        raise HTTPException(status_code=400, detail="No access token in response")

    return token


async def get_userinfo_from_google(request: Request) -> dict:
    """
    Given a request that has been redirected back from Google (with code),
    do the token exchange and fetch user profile info.
    """
    tokens = await exchange_code_for_tokens(request)

    # Google returns ID token as well which contains profile info (OIDC).  
    # Authlib can parse it:
    try:
        userinfo = await oauth.google.parse_id_token(request, tokens)
    except Exception:
        # If parse_id_token fails, fallback to userinfo endpoint
        userinfo_resp = await oauth.google.get("userinfo", token=tokens)
        userinfo_resp.raise_for_status()
        userinfo = userinfo_resp.json()

    return {
        "tokens": tokens,
        "userinfo": userinfo,
    }


async def refresh_google_access_token(refresh_token: str) -> dict:
    """
    Use a stored refresh token to get a new access token.
    If Google issues a new refresh token, it will be in the response too.
    """
    # Token endpoint is discovered from metadata through Authlib
    token_endpoint = oauth.google.client_kwargs.get("token_endpoint") \
                     or "https://oauth2.googleapis.com/token"

    client = oauth.google.create_client()  # underlying AsyncOAuth2Client
    try:
        new_token = await client.refresh_token(
            token_endpoint,
            refresh_token=refresh_token,
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to refresh token: {e}")

    return new_token


def extract_token_values(tokens: dict) -> dict:
    """
    Helper utility to pull out useful values.
    This helps if you want to store tokens/refresh_token in your DB.
    """
    return {
        "access_token": tokens.get("access_token"),
        "refresh_token": tokens.get("refresh_token"),  # may be None if none returned
        "expires_in": tokens.get("expires_in"),
        "id_token": tokens.get("id_token"),
        "scope": tokens.get("scope"),
    }
