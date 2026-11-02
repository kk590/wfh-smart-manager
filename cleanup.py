#!/usr/bin/env python3
"""Cleanup utility for temporary files and caches."""

import os
import shutil
from pathlib import Path

def cleanup():
    patterns = [
        "**/__pycache__",
        "**/*.pyc",
        ".models_cache*.json",
        "frontend/.angular",
        "frontend/node_modules",
    ]
    root = Path(__file__).parent
    for pattern in patterns:
        for path in root.glob(pattern):
            if path.is_dir():
                shutil.rmtree(path, ignore_errors=True)
                print(f"Removed dir: {path}")
            elif path.is_file():
                path.unlink(missing_ok=True)
                print(f"Removed file: {path}")

if __name__ == "__main__":
    cleanup()
