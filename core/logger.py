import logging
import os
from logging.handlers import RotatingFileHandler

# Ensure logs directory exists with absolute path
current_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(current_dir, "..", "logs")
log_dir = os.path.abspath(log_dir)
os.makedirs(log_dir, exist_ok=True)

# Create logger
logger = logging.getLogger("athena-backend")
logger.setLevel(logging.INFO)

# Clear any existing handlers to avoid duplicates
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# Create formatter without unicode characters to avoid encoding issues on Windows
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Create file handler with rotation
log_file_path = os.path.join(log_dir, "athena_backend.log")
file_handler = RotatingFileHandler(
    filename=log_file_path,
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5,
    encoding='utf-8'  # Specify UTF-8 encoding to handle unicode characters
)
file_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Log the file path for debugging
logger.info("Logger initialized. Log file path: %s", log_file_path)