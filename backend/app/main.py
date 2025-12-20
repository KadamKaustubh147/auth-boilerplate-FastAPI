from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from app.api.router import router
from app.db.mongo import init_db
from app.core.config import settings
from app.core.limiter import limiter


# Use lifespan events for intialising Databases or ML models
@asynccontextmanager
async def lifespan(app:FastAPI):
    await init_db()
    
    # yield is necessary as per lifespan syntax
    yield
    # shutdown cleanup (optional)

app = FastAPI(lifespan=lifespan)

app.state.limiter = limiter



app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler) # type:ignore
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)