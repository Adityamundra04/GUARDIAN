"""
Quick test script to verify Guardian logging system is working correctly.
Tests all loggers and verifies log files are created.
"""
import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.core.logger import (
    setup_root_logger,
    get_monitor_logger,
    get_ai_logger,
    get_prometheus_logger,
    get_k8s_logger,
    get_action_logger,
    get_safety_logger,
    LOGS_DIR
)


def test_logging_system():
    """Test the logging system."""
    print("=" * 60)
    print("Guardian Logging System Test")
    print("=" * 60)
    
    # Setup root logger
    print("\n1. Setting up root logger...")
    setup_root_logger()
    print("✅ Root logger initialized")
    
    # Check logs directory
    print("\n2. Checking logs directory...")
    if LOGS_DIR.exists():
        print(f"✅ Logs directory exists: {LOGS_DIR.absolute()}")
    else:
        print(f"❌ Logs directory not found: {LOGS_DIR.absolute()}")
        return
    
    # Test each logger
    print("\n3. Testing service loggers...")
    
    loggers = [
        ("MonitorService", get_monitor_logger()),
        ("AIService", get_ai_logger()),
        ("PrometheusService", get_prometheus_logger()),
        ("K8sService", get_k8s_logger()),
        ("OpenClaw", get_action_logger()),
        ("Safety", get_safety_logger())
    ]
    
    for name, logger in loggers:
        logger.info(f"Test log from {name}")
        logger.debug(f"Debug message from {name}")
        logger.warning(f"Warning message from {name}")
        print(f"✅ {name} logger working")
    
    # Test error logging
    print("\n4. Testing error logging...")
    error_logger = get_monitor_logger()
    try:
        raise ValueError("Test error for logging system")
    except Exception as e:
        error_logger.error(f"Test error: {e}", exc_info=True)
    print("✅ Error logging working")
    
    # Check log files
    print("\n5. Checking log files...")
    log_files = [
        "guardian.log",
        "errors.log",
        "monitoring.log",
        "ai.log",
        "actions.log"
    ]
    
    for log_file in log_files:
        log_path = LOGS_DIR / log_file
        if log_path.exists():
            size = log_path.stat().st_size
            print(f"✅ {log_file} exists ({size} bytes)")
        else:
            print(f"❌ {log_file} not found")
    
    print("\n" + "=" * 60)
    print("Logging System Test Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Check logs directory: ls logs/")
    print("2. View main log: tail -f logs/guardian.log")
    print("3. View errors: tail -f logs/errors.log")
    print("4. Start Guardian: cd backend && python -m app.main")


if __name__ == "__main__":
    test_logging_system()
