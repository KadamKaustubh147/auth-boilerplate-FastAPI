from slowapi import Limiter
from slowapi.util import get_remote_address
from app.accounts.service import get_user_identifier

# get_remote_address gets the client IP address
limiter = Limiter(key_func=get_remote_address)

# user based rate limiting

limiter_user = Limiter(key_func=lambda request: get_user_identifier(request))