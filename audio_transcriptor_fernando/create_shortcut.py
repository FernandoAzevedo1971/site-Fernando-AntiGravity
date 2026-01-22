import os
import winshell
from win32com.client import Dispatch

# Config
EXE_PATH = r"c:\Users\ferna\OneDrive\Documentos\Projetos AntiGravity\audio_transcriptor_fernando\dist\AudioTranscriptor.exe"
WORKING_DIR = os.path.dirname(EXE_PATH)
SHORTCUT_NAME = "AudioTranscriptor.lnk"

# Get Startup Folder
startup_folder = winshell.startup()
shortcut_path = os.path.join(startup_folder, SHORTCUT_NAME)

print(f"Creating shortcut at: {shortcut_path}")

try:
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = EXE_PATH
    shortcut.WorkingDirectory = WORKING_DIR
    shortcut.IconLocation = EXE_PATH
    shortcut.save()
    print("Shortcut created successfully!")
except Exception as e:
    print(f"Error creating shortcut: {e}")
