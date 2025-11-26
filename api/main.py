from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from api.config import settings
from api.routes import predictions

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    predictions.router,
    prefix="/api/v1",
    tags=["Supplier Risk Prediction"]
)

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Supplier Risk Prediction API",
        "version": settings.API_VERSION,
        "status": "running",
        "docs": "/docs",
        "health": "/api/v1/health"
    }

@app.on_event("startup")
async def startup_event():
    logger.info("=" * 60)
    logger.info("API STARTUP")
    logger.info("=" * 60)
    logger.info(f"Title: {settings.API_TITLE}")
    logger.info(f"Version: {settings.API_VERSION}")
    logger.info(f"Model: {settings.MODEL_PATH}")
    logger.info(f"Docs: http://localhost:8000/docs")
    logger.info("=" * 60)

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("API SHUTDOWN")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal server error",
            "detail": str(exc)
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )