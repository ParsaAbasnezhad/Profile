import subprocess
import sys
import webbrowser
import time
from pathlib import Path

project_root = Path(__file__).resolve().parent
subprocess.Popen(
    [sys.executable, "manage.py", "runserver"],
    cwd=project_root,
)

time.sleep(2)

webbrowser.open("http://localhost:8000")