import csv
import logging
import os

from config import EXPORT_DIR

logger = logging.getLogger(__name__)


def export_to_csv(rows, filename="students_export.csv"):
    """Export a list of sqlite3.Row objects to a CSV file."""
    os.makedirs(EXPORT_DIR, exist_ok=True)
    path = os.path.join(EXPORT_DIR, filename)

    if not rows:
        logger.warning("No rows to export.")
        return None

    headers = rows[0].keys()
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in rows:
            writer.writerow([row[h] for h in headers])

    logger.info("Exported %s rows to %s", len(rows), path)
    return path