# ======================================================================================================================
# TimeDisplay
#
# An application that displays time in a window.
#
# Author: TwelfthDoctor1 [TD1]
# License: NIL/TBD~, Likely MIT
# ======================================================================================================================
# Module Importation
import os
from pathlib import Path
from TimeDisplayLib.TimeDisplayHandler import run_GUI
from UtilLib.ConfigJSON import ConfigJSON, setDebugState_Config
from UtilLib.ConfigTemplate import CONFIG_DEFAULT, CONFIG_NAME
# ======================================================================================================================
# DEBUG SETTING
#
# Setting to configure Filepath.
# Files will be saved in the ~ Directory (ref. User Directory)
DEBUG = True

setDebugState_Config(DEBUG, Path(os.path.expanduser("~")).resolve())
# ======================================================================================================================
# Init Settings
# Initialise the Config File for checks
# Should it does not exist, a new file will be created.
config = ConfigJSON(CONFIG_NAME)
config.generate_json(CONFIG_DEFAULT)
# ======================================================================================================================
# Run GUI
run_GUI()
# ======================================================================================================================
