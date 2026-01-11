from fastapi import APIRouter
from app.accounts.router import router as auth_router

router = APIRouter()

# list of app specific routers
router.include_router(auth_router)

print(router.routes)  # Debug: Print the list of routes included in the main router
