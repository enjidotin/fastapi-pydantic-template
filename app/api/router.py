from fastapi import APIRouter

from app.api.routes.items import router as items_router

# Main API router
api_router = APIRouter()

# Include all route modules
api_router.include_router(items_router)

# Add more routers here as the application grows
# api_router.include_router(users_router)
# api_router.include_router(auth_router) 