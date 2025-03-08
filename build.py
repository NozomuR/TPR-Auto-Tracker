import subprocess
import os
import sys


def build_executable():
    python_exe = sys.executable
    sep = ";" if os.name == "nt" else ":"
    add_data_arg = f"items{sep}items"  # include the items folder

    command = [
        python_exe, "-m", "PyInstaller.__main__",
        "--onefile",
        "--windowed",
        "--add-data", add_data_arg,
        "main.py"
    ]

    print("Running command:", " ".join(command))
    subprocess.call(command)


if __name__ == "__main__":
    build_executable()
