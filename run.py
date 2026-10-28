"""
CelebrateAI - Server Entrypoint & Port Discovery
Launches the FastAPI application on an available host port.
"""

import logging
import os
import sys
import socket
from typing import List, Optional
import uvicorn

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("celebrate_ai.server")

# Ensure UTF-8 output encoding on Windows consoles
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def is_port_in_use(port_num: int, host: str = "127.0.0.1") -> bool:
    """Checks whether a specific TCP port is currently bound."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port_num)) == 0


def find_available_port(
    preferred: int = 8080, fallbacks: Optional[List[int]] = None
) -> int:
    """Discovers an unoccupied port starting from preferred to fallback options."""
    if fallbacks is None:
        fallbacks = [8080, 8050, 8000, 8888, 5000]
    env_port = os.getenv("PORT")
    if env_port:
        try:
            return int(env_port)
        except ValueError:
            pass
    for cand in [preferred] + fallbacks:
        if not is_port_in_use(cand):
            return cand
    return preferred


def main() -> None:
    """Launches the CelebrateAI server application."""
    server_port = find_available_port(8080)
    logger.info("CelebrateAI Server initializing on http://127.0.0.1:%s", server_port)
    logger.info("Open http://localhost:%s in your browser to start planning!", server_port)
    uvicorn.run("app.main:app", host="127.0.0.1", port=server_port, reload=False)


if __name__ == "__main__":
    main()
