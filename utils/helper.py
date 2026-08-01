"""General helper utilities."""

import os
import sys
import subprocess
import datetime


def open_file(file_path):
    """Open a file with the system default application."""
    if not os.path.exists(file_path):
        return False
    try:
        if sys.platform == "win32":
            os.startfile(file_path)
        elif sys.platform == "darwin":
            subprocess.call(["open", file_path])
        else:
            subprocess.call(["xdg-open", file_path])
        return True
    except Exception:
        return False


def timestamp_str():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def safe_filename(name):
    return name.replace(" ", "_")
