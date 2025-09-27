# ======================================================================================================================
# TD1 Compile Script
#
# Compile Python Project into an Executable through reference via the main .py file
# ======================================================================================================================
# Module Importation
import os.path
import PyInstaller.__main__
import sys
import time
from pathlib import Path
from sys import platform

# ======================================================================================================================
# Settings
#
# Below are the settings for the compile file.
#
MAIN_PY = "TimeDisplay"  # Name of Main .py file, refer as File Name without extensions
INFO_ADDON = \
    "\t<key>NSRequiresAquaSystemAppearance</key>\n\t<string>False</string>\n"  # Dark Mode KV for Info.plist on macOS
BASE_PATH = Path(__file__).resolve().parent  # Project Filepath
CORE_COMPILE = os.path.join(BASE_PATH, f"{MAIN_PY}.py")  # Reference FP to Main .py file

# ======================================================================================================================
# Determine Compilation Path based on Platform
if platform == "win32":  # Windows
    COMPILE_PATH = os.path.join(BASE_PATH, "CompileBuild", "WIN32")
    DIST_PATH = os.path.join(COMPILE_PATH, "dist")
    BUILD_PATH = os.path.join(COMPILE_PATH, "build")
    RESOURCE_PATH = os.path.join(BASE_PATH, "Resources")
    ICON_PATH = os.path.join(BASE_PATH, "Resources", "TimeDisplayIcon_V2.png")

elif platform == "darwin":  # macOS
    COMPILE_PATH = os.path.join(BASE_PATH, "CompileBuild", "MACOS")
    DIST_PATH = os.path.join(COMPILE_PATH, "dist")
    BUILD_PATH = os.path.join(COMPILE_PATH, "build")
    RESOURCE_PATH = os.path.join(BASE_PATH, "Resources")
    ICON_PATH = os.path.join(BASE_PATH, "Resources", "TimeDisplayIcon_V2.png")

else:  # Supposedly Linux
    # Currently does not support Linux, though the macOS UNIX exec file may suffice (TBD)
    print("[COMPILE_ERROR] Linux currently not supported. Exiting...")

    sys.exit()

print("Compiling TimeDisplay into executable form...")
time.sleep(1)

# ======================================================================================================================
# Run Command to Compile into an Executable file
if platform == "darwin":  # macOS
    # For compiling into an .app
    # Include --windowed flag
    PyInstaller.__main__.run(
        [
            "-D",
            CORE_COMPILE,
            f"-n={MAIN_PY}",
            "--windowed",
            "-y",
            f"--distpath={DIST_PATH}",
            f"--workpath={BUILD_PATH}",
            f"--add-data={RESOURCE_PATH}:Resources",
            f"-i={ICON_PATH}"
        ],
    )
    print("Completed Compilation of file. Editing Info.plist for Dark Mode support...")

    # Edit Info.plist
    plist_fp = os.path.join(DIST_PATH, f"{MAIN_PY}.app", "Contents", "Info.plist")

    with open(plist_fp, "r") as f:
        data = f.read()
        f.close()

    x = data.partition("</dict>")
    y = ""

    for i in range(len(x)):
        y += x[i]
        if i == 0:
            y += INFO_ADDON

    with open(plist_fp, "w") as f:
        f.write(y)
        f.close()

    input("Completed editing of Info.plist file. Press [ENTER] to finish this process...")

else:  # Windows
    # For compiling into .exe
    PyInstaller.__main__.run(
        [
            "-D",
            CORE_COMPILE,
            f"-n={MAIN_PY}",
            "--windowed",
            "-y",
            f"--distpath={DIST_PATH}",
            f"--workpath={BUILD_PATH}",
            f"--add-data={RESOURCE_PATH}:Resources",
            f"-i={ICON_PATH}"
        ],
    )
    # os.system(r"start .\Win32_CompileTimeDisplay.cmd")

    input("Completed compilation of file. Press [ENTER] to finish this process...")
