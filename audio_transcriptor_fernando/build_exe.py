import PyInstaller.__main__
import os

# Define the name of the executable
APP_NAME = "AudioTranscriptor"

# Define the main script
MAIN_SCRIPT = "main.py"

# Define build arguments
args = [
    MAIN_SCRIPT,
    '--name=%s' % APP_NAME,
    '--onefile',
    '--noconsole',
    '--collect-all=customtkinter',
    '--collect-all=tkinterdnd2',
    '--clean',
    '--noconfirm',
]

print(f"Building {APP_NAME}...")
PyInstaller.__main__.run(args)
print(f"Build complete. Executable is located in the 'dist' folder.")
