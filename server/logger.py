import logging
import os

formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s]: %(message)s", "%Y-%m-%d %H:%M:%S"
)
log_level = os.environ.get("LOGLEVEL", "INFO").upper()

# Internal
logger = logging.getLogger()
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(log_level)


# Uvicorn
class HealthEndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return (
            record.args
            and len(record.args) >= 3
            and record.args[2] != "/health"
        )


uvicorn_logger = logging.getLogger("uvicorn.access")
uvicorn_logger.addFilter(HealthEndpointFilter())
for handler in uvicorn_logger.handlers:
    handler.setFormatter(formatter)
uvicorn_logger.setLevel(log_level)
