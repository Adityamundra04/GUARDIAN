"""
Guardian - AI-powered Kubernetes incident assistant
Main FastAPI application entry point
"""

import threading
import time
import logging
from fastapi import FastAPI

from backend.app.api import incidents
from backend.app.services.monitor_service import MonitorService

# -------------------------------
# Logging setup
# -------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------------
# FastAPI App
# -------------------------------
app = FastAPI(
    title="Guardian",
    description="AI-powered Kubernetes incident assistant",
    version="1.0.0"
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
    logger.info("🚀 Guardian monitoring started...")

    while True:
        try:
            monitor_service.monitor_and_create_incidents()
        except Exception as e:
            logger.error(f"❌ Monitoring error: {e}")

        # Always sleep (prevents CPU overuse)
        time.sleep(5)


@app.on_event("startup")
def startup_event():
    """
    Start background monitoring when FastAPI app starts.
    """
    global monitoring_started

    if monitoring_started:
        logger.info("⚠️ Monitoring already running, skipping...")
        return

    monitoring_started = True

    logger.info("🔧 Starting Guardian application...")

    # Start monitoring thread
    monitoring_thread = threading.Thread(
        target=background_monitoring_loop,
        daemon=True
    )
    monitoring_thread.start()

    logger.info("✅ Background monitoring thread started")


# -------------------------------
# API Endpoints
# -------------------------------
@app.get("/")
def root():
    return {"message": "Guardian is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}