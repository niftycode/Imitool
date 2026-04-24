# imitool

A Python tool that displays an image with associated information (filename, file size, camera model and lens used).

## Requirements

For the program to work, the `exiftool` utility must be installed on the system. This utility can be installed on macOS using Homebrew:

```Bash
brew install exiftool
```

## Installation

An executable program for macOS is available for download. Download the ZIP file, extract it, and copy the program to the Program Files folder.

Operating system: macOS
Current version: 0.1.4

Or clone the code, create a virtual environment and installe all packages:

```Bash
pip install -r requirements.txt
```

The program can then be started by executing the file `main.py`.

```Bash
python3 src/main.py
```
