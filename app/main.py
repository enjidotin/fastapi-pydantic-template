from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.adapters.repositories.database import init_db
from app.api.router import api_router
from app.core.config import settings


def create_application() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured FastAPI application
    """
    # Create FastAPI app
    app = FastAPI(
        title=settings.APP_NAME,
        description="FastAPI Hexagonal Architecture Template",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.ALLOWED_HOSTS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API router
    app.include_router(api_router, prefix="/api")

    # Add startup event to initialize database
    @app.on_event("startup")
    async def startup_event():
        await init_db()

    # Add global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal Server Error: {str(exc)}"},
        )

    return app


# Create the application instance
app = create_application()
