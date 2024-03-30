import contextvars
import logging
import os
from datetime import datetime 

request_id_context = contextvars.ContextVar("request_id")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

dt = datetime.now()
unique_time = dt.strftime('%y%m%d%H%M%S')
file_handler = logging.FileHandler(f"logs/{unique_time}_logs.txt")
file_formatter = logging.Formatter(
    fmt="%(asctime)s :: %(filename)-20s :: %(levelname)-6s :: %(lineno)-6s :: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

handler = logging.StreamHandler()

format_mode = os.getenv("LOG_FORMAT", "line")
line_formatter = logging.Formatter(
    fmt=" %(filename)-20s :: %(levelname)-6s :: %(lineno)-6s :: %(message)s"
)
handler.setFormatter(line_formatter)
logger.addHandler(handler)
