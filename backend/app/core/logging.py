import logging
import sys
from app.core.config import settings

def setup_logging():
    """
    Configure professional logging for the entire application.
    Sets the log level based on the DEBUG setting.
    Outputs to standard out with a consistent format.
    """
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO
    
    logging.basicConfig(
        stream=sys.stdout,
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    
    # Silence chatty third-party loggers
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    if settings.DEBUG:
        logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

logger = logging.getLogger(settings.PROJECT_NAME)
