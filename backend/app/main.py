print("Auth router")
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from slowapi.errors import RateLimitExceeded
# from slowapi import _rate_limit_exceeded_handler

from app.api.router import router
from app.db.mongo import init_db
from app.core.config import settings


# Use lifespan events for initialising Databases or ML models
print("Lifespan started")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Lifespan startup: initializing limiter and DB")
    await init_db()
    print("Lifespan startup: complete")
    
    yield
    
    print("Lifespan shutdown: cleanup")

print("Lifespan ended")

# Create app FIRST with lifespan
app = FastAPI(lifespan=lifespan)


# Add exception handler
# app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore

# Add middleware in reverse order (last add = first execute)
# Add CORS last (outermost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include router last
app.include_router(router)

print("FastAPI app initialized successfully")