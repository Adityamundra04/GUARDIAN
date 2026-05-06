"""
Centralized logging configuration for Guardian.
Provides structured logging with file rotation and console output.
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path


# Create logs directory if it doesn't exist
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

# Log file paths
GUARDIAN_LOG = LOGS_DIR / "guardian.log"
ERRORS_LOG = LOGS_DIR / "errors.log"
MONITORING_LOG = LOGS_DIR / "monitoring.log"
AI_LOG = LOGS_DIR / "ai.log"
ACTIONS_LOG = LOGS_DIR / "actions.log"

# Log format
LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Global logging level
LOG_LEVEL = logging.INFO


def create_rotating_handler(log_file: Path, max_bytes: int = 5 * 1024 * 1024, backup_count: int = 5) -> RotatingFileHandler:
    """
    Create a rotating file handler.
    
    Args:
        log_file: Path to log file
        max_bytes: Maximum file size before rotation (default: 5MB)
        backup_count: Number of backup files to keep (default: 5)
    
    Returns:
        Configured RotatingFileHandler
    """
    handler = RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
    return handler


def create_console_handler() -> logging.StreamHandler:
    """
    Create a console handler for terminal output.
    
    Returns:
        Configured StreamHandler
    """
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
    return handler


def get_logger(name: str, log_to_file: str = None) -> logging.Logger:
    """
    Get or create a logger with the specified name.
    
    Args:
        name: Logger name (typically service name)
        log_to_file: Optional specific log file ('monitoring', 'ai', 'actions')
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    logger.setLevel(LOG_LEVEL)
    logger.propagate = False
    
    # Add console handler (always)
    logger.addHandler(create_console_handler())
    
    # Add main guardian.log handler (always)
    logger.addHandler(create_rotating_handler(GUARDIAN_LOG))
    
    # Add errors.log handler for ERROR and above
    error_handler = create_rotating_handler(ERRORS_LOG)
    error_handler.setLevel(logging.ERROR)
    logger.addHandler(error_handler)
    
    # Add service-specific log file if specified
    if log_to_file == 'monitoring':
        logger.addHandler(create_rotating_handler(MONITORING_LOG))
    elif log_to_file == 'ai':
        logger.addHandler(create_rotating_handler(AI_LOG))
    elif log_to_file == 'actions':
        logger.addHandler(create_rotating_handler(ACTIONS_LOG))
    
    return logger


def setup_root_logger():
    """
    Setup root logger for Guardian application.
    Called once at application startup.
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(LOG_LEVEL)
    
    # Clear any existing handlers
    root_logger.handlers.clear()
    
    # Add console handler
    root_logger.addHandler(create_console_handler())
    
    # Add main log file handler
    root_logger.addHandler(create_rotating_handler(GUARDIAN_LOG))
    
    # Add error log file handler
    error_handler = create_rotating_handler(ERRORS_LOG)
    error_handler.setLevel(logging.ERROR)
    root_logger.addHandler(error_handler)
    
    # Log startup message
    root_logger.info("=" * 60)
    root_logger.info("Guardian Application Started")
    root_logger.info("=" * 60)
    root_logger.info(f"Logs directory: {LOGS_DIR.absolute()}")
    root_logger.info(f"Main log: {GUARDIAN_LOG}")
    root_logger.info(f"Error log: {ERRORS_LOG}")
    root_logger.info(f"Monitoring log: {MONITORING_LOG}")
    root_logger.info(f"AI log: {AI_LOG}")
    root_logger.info(f"Actions log: {ACTIONS_LOG}")


# Convenience function for getting common loggers
def get_monitor_logger() -> logging.Logger:
    """Get logger for MonitorService."""
    return get_logger("MonitorService", log_to_file='monitoring')


def get_ai_logger() -> logging.Logger:
    """Get logger for AIService."""
    return get_logger("AIService", log_to_file='ai')


def get_prometheus_logger() -> logging.Logger:
    """Get logger for PrometheusService."""
    return get_logger("PrometheusService", log_to_file='monitoring')


def get_k8s_logger() -> logging.Logger:
    """Get logger for K8sService."""
    return get_logger("K8sService", log_to_file='monitoring')


def get_action_logger() -> logging.Logger:
    """Get logger for ActionExecutor (OpenClaw)."""
    return get_logger("OpenClaw", log_to_file='actions')


def get_safety_logger() -> logging.Logger:
    """Get logger for SafetyRules."""
    return get_logger("Safety", log_to_file='actions')
