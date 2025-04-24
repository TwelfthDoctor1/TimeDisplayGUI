import os
from pathlib import Path

# Authoring, Attributes and Licensing
__author__ = "TwelfthDoctor1"
__copyright__ = "Copyright 2020: MasterApprentice Logger Project | © TD1 & TWoCC 2020-2023"
__credits__ = "TwelfthDoctor1"
__license__ = "CC 4.0 or MIT"


# Version Control Datum
__version__ = "Developer Version 1.5.0"
__status__ = "Development Testing"


class MasterApprenticeLogVersionType:
    DEVELOPER = 0
    BETA = 1
    RELEASE = 2


def setDebugState_Log(state: bool, mlog_bypass: bool = False, bypass_fp: Path or str = "", author: str = ""):
    """
    Method to set the filepath for logging.
    :param author:
    :param bypass_fp:
    :param state:
    :param mlog_bypass:
    :return:
    """
    if state is False:
        global master_logger_enabler
        global apprentice_version_type
        global master_version_type
        global MAIN_DIR
        global AUTHOR

        apprentice_version_type = MasterApprenticeLogVersionType.RELEASE
        master_version_type = MasterApprenticeLogVersionType.RELEASE

        if mlog_bypass is False:
            master_logger_enabler = False

        if bypass_fp != "":
            MAIN_DIR = bypass_fp

        else:
            MAIN_DIR = MAIN_DIR.parent

        if author != "":
            AUTHOR = author


# Main Path File for Project
# Set .parent level if MasterApprentice Library is nested
MAIN_DIR = Path(__file__).resolve().parent.parent
FILENAME = "TimeDisplay"
AUTHOR = __author__


# The Version Type of Master Apprentice Logger
master_version_type = MasterApprenticeLogVersionType.DEVELOPER
apprentice_version_type = MasterApprenticeLogVersionType.DEVELOPER

# Enabler for the Master Logger
# Leave this as [False] for release versions
master_logger_enabler = True

# Delete old ApprenticeLogger Logs
delete_old_apprentice_log = True

# Delete old MasterLogger Logs
delete_old_master_log = True

setDebugState_Log(True, False, Path(os.path.expanduser("~")).resolve())
