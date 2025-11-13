# ======================================================================================================================
# TimeDisplay
#
# An application that displays time in a window.
#
# Author: TwelfthDoctor1 [TD1]
# License: NIL/TBD~, Likely MIT
# ======================================================================================================================
# Module Importation
import argparse
import os
import sys
from pathlib import Path
from MasterApprenticeLib.TD1_Lib_MasterApprentice_Control import setDebugState_Log
from TimeDisplayLib.TimeDisplayHandler import run_GUI, run_MiniGUI
from UtilLib.ConfigJSON import ConfigJSON, setDebugState_Config
from UtilLib.ConfigTemplate import CONFIG_DEFAULT, CONFIG_NAME
# ======================================================================================================================
# ARGUMENT PARSER
parser = argparse.ArgumentParser(
    description="TimeDisplay - Displays the current time.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

# PARSER FLAGS
parser.add_argument(
    "--mini-ui",
    help="Force the use of Mini-UI whilst ignoring useMiniUI config value",
    action="store_true",
    default=False,
    required=False,
    dest="mini_ui"
)
parser.add_argument(
    "--reg-ui",
    help="Force the use of Reg-UI whilst ignoring useMiniUI config value",
    action="store_true",
    default=False,
    required=False,
    dest="reg_ui"
)
parser.add_argument(
    "--debug-config", "--d-c",
    help="Enable Config debugging by redirecting config file path to exec location rather than ~/",
    action="store_true",
    default=False,
    required=False
)
# parser.add_argument(
#     "--debug-log", "--d-l",
#     help="Enable debugging by enabling log file creation",
#     action="store_true",
#     default=False,
#     required=False
# )
# parser.add_argument(
#     "--debug-mlog", "--d-m",
#     help="Enable MasterLogger for debugging in console",
#     action="store_true",
#     default=False,
#     required=False
# )

cmd_args = parser.parse_args(sys.argv[1:])
# ======================================================================================================================
# DEBUG SETTINGS
#
# Setting to configure Filepath for Config, use of Logging for Debugging.
# Files will be saved in the ~ Directory (ref. User Directory)
DEBUG_CONFIG = False or cmd_args.debug_config
# DEBUG_LOG = False or cmd_args.debug_log
# DEBUG_ENABLE_MLOG = False # or cmd_args.debug_mlog

setDebugState_Config(DEBUG_CONFIG, Path(os.path.expanduser("~")).resolve())
# setDebugState_Log(DEBUG_LOG, DEBUG_ENABLE_MLOG, Path(os.path.expanduser("~")).resolve())
# ======================================================================================================================
# Init Settings
# Initialise the Config File for checks
# Should it does not exist, a new file will be created.
config = ConfigJSON(CONFIG_NAME)
config.generate_json(CONFIG_DEFAULT)
# ======================================================================================================================
# Run GUI
if cmd_args.mini_ui:
    run_MiniGUI()
elif cmd_args.reg_ui:
    run_GUI()
elif not config.return_specific_json("useMiniUI"):
    run_GUI()
else:
    run_MiniGUI()
# ======================================================================================================================

