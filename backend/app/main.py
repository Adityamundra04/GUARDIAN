"""
Guardian - AI-powered Kubernetes incident assistant
Main FastAPI application entry point
"""
from fastapi import FastAPI
from backend.app.api import incidents

# Create FastAPI application
app = FastAPI(
    title="Guardian",
    description="AI-powered Kubernetes incident assistant",
    version="1.0.0"
)

# Include incident router
app.include_router(incidents.router)


@app.get("/")
async def root() -> dict:
    """
    Root endpoint - health check message.
    
    Returns:
        Welcome message confirming Guardian is running
    """
    return {"message": "Guardian is running"}


@app.get("/health")
async def health_check() -> dict:
    """
    Health check endpoint for monitoring.
    
    Returns:
        Status indicating service health
    """
    return {"status": "ok"}
