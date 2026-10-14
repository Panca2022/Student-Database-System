import logging
import sys

from config import LOG_LEVEL


def setup_logging():
    logging.basicConfig(
        level=LOG_LEVEL,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("student_app.log", encoding="utf-8"),
        ],
    )
    