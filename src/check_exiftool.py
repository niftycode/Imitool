#!/usr/bin/env python3

"""
This module checks if ExifTool is available on the system.
Version: 1.0
Python 3.14
Date created: März 26, 2026
Date modified: -
"""

import tkinter as tk
from tkinter import messagebox


def check_exiftool_available(root: tk.Tk) -> bool:
    exiftool_path = "/opt/homebrew/bin/exiftool"
    if exiftool_path is None:
        messagebox.showwarning(
            "ExifTool fehlt",
            "ExifTool wurde nicht gefunden.\n\n"
            "Bitte installieren Sie dieses Tool, bevor Sie fortfahren.",
        )
        root.destroy()
        return False
    return True
