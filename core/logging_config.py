"""JSON logging configuration for game-hub — delegates to silrod_core."""

import os

try:
    from silrod_core.logging import setup_logging as silrod_setup_logging
    _has_silrod = True
except ImportError:
    _has_silrod = False

if _has_silrod:
    def setup_logging(level: str = "INFO") -> None:
        silrod_setup_logging(level=level)
else:
    import json
    import logging
    import sys
    from datetime import datetime, timezone

    class JSONFormatter(logging.Formatter):
        def format(self, record: logging.LogRecord) -> str:
            app_name = os.environ.get("SILROD_APP_NAME", "game-hub")
            payload = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
                "app": app_name,
            }
            if record.exc_info and record.exc_info[0]:
                payload["exception"] = self.formatException(record.exc_info)
            return f"{json.dumps(payload)}\n"

    def setup_logging(level: str = "INFO") -> None:
        root = logging.getLogger()
        root.setLevel(getattr(logging, level.upper(), logging.INFO))
        for h in root.handlers[:]:
            root.removeHandler(h)
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(JSONFormatter())
        root.addHandler(handler)
        logging.getLogger("uvicorn").setLevel(logging.WARNING)
        logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
        logging.getLogger("socketio").setLevel(logging.WARNING)
        logging.getLogger("engineio").setLevel(logging.WARNING)
