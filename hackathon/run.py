"""
Single-command launcher for the Nepal Population Health Intelligence Platform.

Usage:
    python run.py

Starts both the FastAPI backend (port 8000) and Streamlit dashboard (port 8502).
Press Ctrl+C to stop both servers.
"""

import subprocess
import sys
import time
import signal

def main():
    print("=" * 60)
    print("  Nepal Population Health Intelligence Platform")
    print("=" * 60)
    print()
    print("  Starting backend API on    http://localhost:8000")
    print("  Starting dashboard on      http://localhost:8502")
    print()
    print("  Press Ctrl+C to stop both servers.")
    print("=" * 60)

    # Start FastAPI backend
    backend = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.main:app", "--reload", "--port", "8000"],
        cwd=sys.path[0] or ".",
    )

    # Small delay so backend starts first
    time.sleep(2)

    # Start Streamlit dashboard
    dashboard = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "dashboard/app.py", "--server.port", "8502"],
        cwd=sys.path[0] or ".",
    )

    def shutdown(sig, frame):
        print("\n\nShutting down servers...")
        backend.terminate()
        dashboard.terminate()
        backend.wait()
        dashboard.wait()
        print("Both servers stopped.")
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    # Wait for either process to exit
    try:
        while True:
            if backend.poll() is not None:
                print("Backend stopped unexpectedly. Shutting down dashboard...")
                dashboard.terminate()
                break
            if dashboard.poll() is not None:
                print("Dashboard stopped unexpectedly. Shutting down backend...")
                backend.terminate()
                break
            time.sleep(1)
    except KeyboardInterrupt:
        shutdown(None, None)


if __name__ == "__main__":
    main()
