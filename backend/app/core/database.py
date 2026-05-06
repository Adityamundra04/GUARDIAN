"""
Database configuration for Guardian.
Provides SQLite connection and SQLAlchemy session management.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pathlib import Path
from backend.app.core.logger import get_logger

# Initialize logger
logger = get_logger("Database")

# Database file location
DB_DIR = Path("data")
DB_DIR.mkdir(exist_ok=True)
DATABASE_FILE = DB_DIR / "guardian.db"
DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

# SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Needed for SQLite
    echo=False  # Set to True for SQL query logging
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()


def get_db() -> Session:
    """
    Get database session.
    Use as dependency injection in FastAPI endpoints.
    
    Yields:
        Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_database():
    """
    Initialize database and create all tables.
    Called on application startup.
    """
    try:
        logger.info(f"Initializing database: {DATABASE_FILE}")
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        logger.info("Database initialized successfully")
        logger.info(f"Database location: {DATABASE_FILE.absolute()}")
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}", exc_info=True)
        raise


def get_db_session() -> Session:
    """
    Get a new database session.
    Use for manual session management outside FastAPI.
    
    Returns:
        Database session (remember to close it)
    """
    return SessionLocal()
