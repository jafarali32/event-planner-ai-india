"""
CelebrateAI - Server Entrypoint & Port Discovery
Launches the FastAPI application on an available host port.
"""

import os
import sys
import socket
from typing import List
import uvicorn

# Ensure UTF-8 output encoding on Windows consoles
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def is_port_in_use(port: int, host: str = "127.0.0.1") -> bool:
    """Checks whether a specific TCP port is currently bound."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0

def find_available_port(preferred: int = 8080, fallbacks: List[int] = None) -> int:
    """Discovers an unoccupied port starting from preferred to fallback options."""
    if fallbacks is None:
        fallbacks = [8080, 8050, 8000, 8888, 5000]
    env_port = os.getenv("PORT")
    if env_port:
        try:
            return int(env_port)
        except ValueError:
            pass
    for port in [preferred] + fallbacks:
        if not is_port_in_use(port):
            return port
    return preferred

if __name__ == "__main__":
    port = find_available_port(8080)
    print("=" * 60)
    print("CelebrateAI - GenAI Event Planning Assistant")
    print(f"Server starting at http://127.0.0.1:{port}")
    print(f"Open http://localhost:{port} in your browser to start planning!")
    print("=" * 60)
    uvicorn.run("app.main:app", host="127.0.0.1", port=port, reload=False)
