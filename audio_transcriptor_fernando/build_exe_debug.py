import PyInstaller.__main__
import os

# Define the name of the executable
APP_NAME = "AudioTranscriptor_Debug"

# Define the main script
MAIN_SCRIPT = "main.py"

# Define build arguments - WITH CONSOLE for debugging
args = [
    MAIN_SCRIPT,
    '--name=%s' % APP_NAME,
    '--onefile',
    '--console',  # Show console window for debug output
    '--collect-all=customtkinter',
    '--collect-all=tkinterdnd2',
    '--clean',
    '--noconfirm',
]

print(f"Building {APP_NAME} with console enabled for debugging...")
PyInstaller.__main__.run(args)
print(f"Build complete. Executable is located in the 'dist' folder.")
print(f"This version shows a console window with debug logs.")
