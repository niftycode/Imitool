#!/usr/bin/env python3

"""
This is a simple GUI application that displays the size of an image.
Version: 1.0
Python 3.14
Date created: March 26, 2026
Date modified: April 4th, 2026
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, ttk

import pillow_heif
from PIL import Image, ImageTk

from src import about_window, check_exiftool, metadata

# from pillow_heif import register_heif_opener


class MainWindow:
    def __init__(self) -> None:

        self.window = tk.Tk()
        self.window.title("Imitool")

        window_width = 800
        window_height = 600

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        self.window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        self.window.resizable(True, True)

        # Hauptcontainer für Bild und Informationen
        self.content_frame = ttk.Frame(self.window)
        self.content_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Linker Bereich für das Bild
        self.image_label = tk.Label(self.content_frame, text="Kein Bild ausgewählt")
        self.image_label.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # Rechter Bereich für die Informationen
        self.info_frame = tk.Frame(self.content_frame)
        self.info_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))

        self.info_title_label = ttk.Label(
            self.info_frame, text="Image information:", font=("Arial", 12, "bold")
        )
        self.info_title_label.pack(anchor=tk.W)

        self.filename_label = ttk.Label(
            self.info_frame, text="File name: -", anchor=tk.W
        )
        self.filename_label.pack(fill=tk.X)

        self.dimensions_label = ttk.Label(
            self.info_frame, text="Resolution: -", anchor=tk.W
        )
        self.dimensions_label.pack(fill=tk.X)

        self.filesize_label = ttk.Label(
            self.info_frame, text="File size: -", anchor=tk.W
        )
        self.filesize_label.pack(fill=tk.X)

        self.camera_model_label = ttk.Label(
            self.info_frame, text="Camera: -", anchor=tk.W
        )
        self.camera_model_label.pack(fill=tk.X)

        self.lens_label = ttk.Label(self.info_frame, text="Lens: -", anchor=tk.W)
        self.lens_label.pack(fill=tk.X)

        # Container
        self.button_frame = ttk.Frame(self.window)
        self.button_frame.pack(side=tk.BOTTOM, pady=10)

        self.select_button = ttk.Button(
            self.button_frame, text="Select an image", command=self.load_image
        )
        self.select_button.grid(row=0, column=0, padx=5)

        # Add a button to open the about window
        self.about_button = ttk.Button(
            self.button_frame,
            text="About",
            command=lambda: about_window.show_custom_about(),
        )
        self.about_button.grid(row=0, column=1, padx=5)

        # Add a button to quit the application
        self.quit_button = ttk.Button(
            self.button_frame, text="Quit", command=self.quit_program
        )
        self.quit_button.grid(row=0, column=2, padx=5)

        self.current_photo = None

        # Check if Finder has passed a file
        self.window.after(100, self.open_from_argv_if_present)

        # macOS-specific handler for opening documents
        if sys.platform == "darwin":
            self.window.createcommand(
                "::tk::mac::OpenDocument", self.macos_open_document
            )

        if not check_exiftool.check_exiftool_available(self.window):
            self.window.destroy()
            return

    def open_from_argv_if_present(self):
        args = [a for a in sys.argv[1:] if not a.startswith("-psn_")]  # macOS
        if args:
            self.load_image(args[0])

    def macos_open_document(self, *args):
        for arg in args:
            if arg:
                self.load_image(arg)
                break  # Only load the first file

    def load_image(self, file_path=None):
        if file_path is None:
            filetypes = [
                ("Image files", "*.png *.jpg *.jpeg *.heic *.HEIC *.heif *.HEIF"),
                ("PNG", "*.png"),
                ("JPEG", "*.jpg *.jpeg"),
                ("All files", "*.*"),
            ]
            file_path = filedialog.askopenfilename(
                title="Select image", filetypes=filetypes
            )

        if not file_path:
            return

        try:
            pillow_heif.register_heif_opener()

            pil_image = Image.open(file_path)
            orig_width, orig_height = pil_image.size
            filename = os.path.basename(file_path)

            # Invoke the metadata module to get the file size
            size_mb = metadata.get_file_size(file_path)

            # Invoke the metadata module to get the camera and lens info
            camera_model, lens = metadata.get_camera_info(file_path)

            # Scale image to fit window if too large
            max_width = 800
            max_height = 600

            # Use current window size as reference or default values
            width, height = pil_image.size
            if width > max_width or height > max_height:
                pil_image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

            self.current_photo = ImageTk.PhotoImage(pil_image)
            self.image_label.config(image=self.current_photo, text="")

            self.filename_label.config(text=f"File name: {filename}")
            self.dimensions_label.config(
                text=f"Resolution: {orig_width} x {orig_height} px"
            )
            self.filesize_label.config(text=f"File size: {size_mb:.2f} MB")

            # Camera and lens info
            self.camera_model_label.config(text=f"Camera: {camera_model}")
            self.lens_label.config(text=f"Lens: {lens}")

            # Adjust window size based on image size
            new_width = max(800, pil_image.width + 250)  # +250 for info section
            new_height = max(600, pil_image.height + 80)  # +80 for button and padding
            self.window.geometry(f"{new_width}x{new_height}")

        except Exception as e:
            from tkinter import messagebox

            messagebox.showerror("Error", f"Image could not be loaded: {e}")

    def quit_program(self):
        """
        Destroys the main application window.

        This method is used to terminate the application by closing the primary window. It leverages the `destroy` method of the `tkinter` library to shut down the interface and safely exit the program.

        Raises:
            None
        """
        self.window.destroy()

    def mainloop(self):
        self.window.mainloop()


if __name__ == "__main__":
    app_instance = MainWindow()
    app_instance.mainloop()
