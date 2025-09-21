
from __future__ import annotations
import logging, json, sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_json_logger(name: str = "suite", log_dir: str | None = None, fname: str = "suite.jsonl", max_bytes: int = 1_000_000, backup_count: int = 3):
    log_dir = Path(log_dir or ("tmp/logs"))
    log_dir.mkdir(parents=True, exist_ok=True)
    path = log_dir / fname
    handler = RotatingFileHandler(path, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8")
    class JsonFormatter(logging.Formatter):
        def format(self, record: logging.LogRecord):
            payload = {
                "level": record.levelname,
                "name": record.name,
                "msg": record.getMessage(),
                "ts": self.formatTime(record),
            }
            return json.dumps(payload, ensure_ascii=False)
    handler.setFormatter(JsonFormatter())
    logger = logging.getLogger(name)
    logger.handlers.clear()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    # mirror to stderr for convenience
    stderr = logging.StreamHandler(sys.stderr)
    stderr.setFormatter(JsonFormatter())
    logger.addHandler(stderr)
    return logger, path
