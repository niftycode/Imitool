#!/usr/bin/env python3

"""
This module reads the file size of an image using exiftool.
Version: 1.0
Python 3.14
Date created: März 26, 2026
Date modified: -
"""

import json
import subprocess
from pathlib import Path


def get_file_size(file_path: str) -> int:
    file_path = str(Path(file_path).expanduser().resolve())

    cmd = ["/opt/homebrew/bin/exiftool", "-j", "-FileSize#", file_path]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)

    data = json.loads(result.stdout)
    size_bytes = data[0]["FileSize"]
    size_mb = size_bytes / (1024 * 1024)

    return size_mb
    # return data[0]["FileSize"]


def get_camera_info(file_path: str) -> tuple[str, str]:
    cmd = [
        "/opt/homebrew/bin/exiftool",
        "-j",
        "-Model",
        "-LensModel",
        "-LensID",
        file_path,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(result.stdout)[0]

    camera = data.get("Model")
    lens = data.get("LensModel") or data.get("LensID")

    if lens and "|" in lens:
        lens = lens.replace("|", "\n")

    return camera, lens
