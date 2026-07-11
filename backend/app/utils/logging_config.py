import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(log_level=logging.INFO):
    """Configures centralized logging to output to both console and a rolling file."""
    log_format = logging.Formatter(
        '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)d] - %(message)s'
    )
    
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Clear existing handlers to prevent duplicate logs (e.g. from uvicorn initialization)
    if root_logger.hasHandlers():
        root_logger.handlers.clear()
        
    # 1. Console stream handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    root_logger.addHandler(console_handler)
    
    # 2. Rolling file handler (10MB maximum, rolling up to 5 historical log files)
    log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    log_file = os.path.join(log_dir, "app.log")
    
    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=10 * 1024 * 1024, 
        backupCount=5, 
        encoding="utf-8"
    )
    file_handler.setFormatter(log_format)
    root_logger.addHandler(file_handler)
    
    logging.info("Centralized logging configured successfully. Writing to app.log")
