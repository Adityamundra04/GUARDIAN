"""
Guardian - AI-powered Kubernetes incident assistant
Main FastAPI application entry point
"""
from fastapi.middleware.cors import CORSMiddleware
import threading
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api import incidents
from backend.app.services.monitor_service import MonitorService
from backend.app.core.logger import setup_root_logger, get_logger
from backend.app.core.database import init_database

# -------------------------------
# Logging setup
# -------------------------------
setup_root_logger()
logger = get_logger("Guardian")

# -------------------------------
# FastAPI App
# -------------------------------
app = FastAPI(
    title="Guardian",
    description="AI-powered Kubernetes incident assistant",
    version="1.0.0"
)

# -------------------------------
# CORS Middleware
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",  # Vite default port
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(incidents.router)

# -------------------------------
# Monitoring Setup
# -------------------------------
monitor_service = MonitorService()

# Prevent multiple threads (important for reload mode)
monitoring_started = False


def background_monitoring_loop():
    """
    Background thread that continuously monitors Kubernetes cluster.
    Runs every 5 seconds and creates incidents automatically.
    """
    logger.info("Guardian monitoring thread started")

    while True:
        try:
            monitor_service.monitor_and_create_incidents()
        except Exception as e:
            logger.error(f"Monitoring error: {e}", exc_info=True)

        # Always sleep (prevents CPU overuse)
        time.sleep(5)


@app.on_event("startup")
def startup_event():
    """
    Start background monitoring when FastAPI app starts.
    """
    global monitoring_started

    if monitoring_started:
        logger.warning("Monitoring already running, skipping...")
        return

    monitoring_started = True

    logger.info("Starting Guardian application...")
    
    # Initialize database
    try:
        init_database()
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}", exc_info=True)
        # Continue anyway - monitoring can still work

    # Start monitoring thread
    monitoring_thread = threading.Thread(
        target=background_monitoring_loop,
        daemon=True
    )
    monitoring_thread.start()

    logger.info("Background monitoring thread started successfully")


# -------------------------------
# API Endpoints
# -------------------------------
@app.get("/")
def root():
    return {"message": "Guardian is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}