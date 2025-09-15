# ======================================================================================================================
# DEFAULT CONFIGURATION FILE
# This is the default settings for the config file (in .json)
#
# JSON Methodology make use of Python Dictionaries, thereby simplifying
# addition, deletion, and modification processes.
#
# Ensure that the keys are UNIQUE. Also ensure that the keys in code FULLY MATCH
# those written here, or else an error will occur inferring that the key does not exist.
#
# Default values can either be set from here for in UI via value. However, it is recommended to do it here instead.

CONFIG_NAME = "TimeDisplay_Config"  # Name of Config File
CONFIG_DEFAULT = {
    "fontType": None,  # The font to use on the application
    "is24Hr": False,  # Whether the time should be displayed in 12-hour mode or in 24-hour mode
    "darkMode": True,  # Whether the application should be displayed in light mode or in dark mode (TBD)
    "isFloating": False,  # Whether the window is floating
    "fontSizeTime": 70,  # The font size of the Time Display
    "fontSize12Hr": 50,  # The font size of the 12-Hour (AM/PM) identifier, if it is bigger than the size for time,
                         # use TimeSize - 20
    "fontSizeDate": 30,  # The Font size of the Date Display
    "showHr12": True,  # Whether the AM/PM should show in 12-Hour Format
    "showSecs": True,  # Whether the seconds should be shown
    "showDate": True,  # Whether the date should be shown
    "memHWindowSize": 0,  # Horizontal Window Size Memory
    "memVWindowSize": 0,  # Vertical Window Size Memory
    "windowVisibility": 100,  # Window Visibility
    "framelessWindowBar": False, # Set Frameless Window Bar
    "useNativeTheme": False,  # Use Native Theme - Use OS Theme Colours or Light/Dark Mode
    "useBoldFont": False,  # Use Bold Font - if Regular Font is not strong enough for illustration
    "fontWeight": "Normal"  # Font Weight
}
# ======================================================================================================================
