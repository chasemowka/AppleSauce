#!/usr/bin/env python3
"""
Server restart script for AppleSauce backend
Kills any existing process on port 8000 and starts fresh

Usage:
    python restart.py          # Start on default port 8000
    python restart.py 8001     # Start on custom port
"""
import subprocess
import sys
import os
import time

DEFAULT_PORT = 8000


def kill_port(port: int) -> bool:
    """Kill process using the specified port (Windows)"""
    try:
        # Find PID using netstat
        result = subprocess.run(
            f'netstat -ano | findstr :{port}',
            shell=True,
            capture_output=True,
            text=True
        )

        if result.stdout:
            lines = result.stdout.strip().split('\n')
            pids = set()
            for line in lines:
                parts = line.split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    if pid.isdigit():
                        pids.add(pid)

            for pid in pids:
                print(f"Killing process {pid} on port {port}...")
                subprocess.run(f'taskkill /PID {pid} /F', shell=True, capture_output=True)

            if pids:
                time.sleep(1)  # Wait for port to be released
                return True

        return False
    except Exception as e:
        print(f"Error killing port: {e}")
        return False


def start_server(port: int):
    """Start the FastAPI server"""
    # Ensure we're in the backend directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    print(f"\n🚀 Starting AppleSauce API on http://127.0.0.1:{port}")
    print(f"📚 API Docs: http://127.0.0.1:{port}/docs")
    print("Press CTRL+C to stop\n")

    # Start uvicorn
    os.system(f'python -m uvicorn main:app --host 127.0.0.1 --port {port} --reload')


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT

    print(f"🔄 Checking for existing process on port {port}...")
    killed = kill_port(port)

    if killed:
        print(f"✅ Cleared port {port}")
    else:
        print(f"✅ Port {port} is available")

    start_server(port)


if __name__ == "__main__":
    main()
