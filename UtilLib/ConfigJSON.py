# ======================================================================================================================
# Module Importation
from pathlib import Path
from UtilLib.JSONHandler import JSONHandler, JSON_LIB
from UtilLib.ConfigTemplate import CONFIG_DEFAULT, CONFIG_NAME

# ======================================================================================================================
# JSON Path
#
CONFIG_PATH = Path(JSON_LIB).resolve().parent


# ======================================================================================================================
# ConfigJSON Class
class ConfigJSON(JSONHandler):
    """
    A Configuration Handler that borrows functions from JSONHandler.
    """
    def __init__(self, cfg_name: str):
        """
        Initialise the ConfigJSON Class & generate the Config file if required.
        """
        super(ConfigJSON, self).__init__(cfg_name, CONFIG_PATH)
        self.generate_config()

    def generate_config(self):
        """
        Generate the Config JSON. Avoids usage of generate_json().
        :return:
        """
        # Generate Config
        status = self.generate_json(CONFIG_DEFAULT)
        self.getConfigData()

        # Key Check on Existing Config
        if status is False:
            key_check_list = list(self.json_data.keys())
            missing_keys = []
            for key_def in CONFIG_DEFAULT.keys():
                has_checked = False
                for key_check in key_check_list:
                    if key_def == key_check:
                        self.logger.debug(f"DEBUG: CHECK -> {key_def}")
                        key_check_list.remove(key_check)
                        has_checked = True

                if has_checked is False:
                    missing_keys.append(key_def)

            self.logger.debug(f"DEBUG: KEYCHECK MISSING {len(missing_keys)} KEYS: {missing_keys}")

            # Add missing keys
            if len(missing_keys) > 0:
                self.logger.info(f"Config Check: {len(missing_keys)} keys missing. Appending...\n\n{missing_keys}")

                for key in missing_keys:
                    self.json_data[key] = CONFIG_DEFAULT[key]

                # Update File for future reads
                self.update_json_file()
                self.logger.info(f"Config Check: Updated JSON File {self.json_fp}")
            else:
                self.logger.info(f"Config Check: All keys accounted for. No key appending required.")

    def getConfigData(self):
        """
        Alternate call method to get Config Data.

        :return:
        """
        self.formulate_json()


def setDebugState_Config(state: bool, fp: Path or str = ""):
    """
    Method to set Filepath of Config JSON File.
    :param fp:
    :param state:
    :return:
    """
    if state is False:
        global CONFIG_PATH
        if fp == "":
            CONFIG_PATH = CONFIG_PATH.parent
        else:
            CONFIG_PATH = fp
