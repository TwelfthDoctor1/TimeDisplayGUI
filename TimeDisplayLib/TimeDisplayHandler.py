import datetime
import sys
from PyQt6 import QtCore
from PyQt6.QtCore import QTimer, Qt, QSize
from PyQt6.QtGui import QFont, QResizeEvent
from PyQt6.QtWidgets import QMainWindow, QApplication, QDialog
from Qt6UI.QtStyleSheet import QT_STYLESHEET_DARK, QT_STYLESHEET_LIGHT
from Qt6UI.TimeDisplaySettings import Ui_Settings
from Qt6UI.TimeDisplayUI import Ui_TimeDisplay
from UtilLib.ConfigJSON import ConfigJSON, CONFIG_NAME


if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class TimeDisplayGUI(QMainWindow):
    def __init__(self, parent=None):
        super(TimeDisplayGUI, self).__init__(parent)
        self.ui = Ui_TimeDisplay()
        self.hide()  # Initial Hiding

        # Setup UI
        self.ui.setupUi(self)
        self.setWindowTitle("TimeDisplay")
        self._connectActions()
        # self.setStyleSheet(QT_STYLESHEET_LIGHT)

        # Config Data
        self.json = ConfigJSON(CONFIG_NAME)
        self.json.getConfigData()

        # Run Settings
        self.initResize()
        self.updateSettingState()
        self.onFloatChange()
        self.onSwitchTheme()
        self.onUpdateWinVisibility()
        self.onUpdateWindowBar()

        # Menubar - macOS Disabling (FOR TEST ONLY)
        if sys.platform == "darwin":
            # Leave disabled, always use Native Menu Bar
            # self.ui.menubar.setNativeMenuBar(False)
            # self.setWindowFlag(Qt.WindowType.Window.MacWindowToolBarButtonHint, False)
            pass

        # Hotkey - Non macOS -> use Alt+S instead of CMD key
        if sys.platform != "darwin":
            self.ui.action_Settings.setShortcut("Alt+S")

        # Misc Testing Section
        self.ui.statusbar.setVisible(False)

        # Timer to Refresh UI
        self.timer = QTimer()
        self.timer.timeout.connect(self.getTime)
        self.timer.setInterval(10)
        self.timer.start()

    def _connectActions(self):
        self.ui.action_Settings.triggered.connect(self.openSettings)
        self.ui.action_Float_on_Top.triggered.connect(self.settingFloat)
        self.ui.actionUse_24_Hour_Format.triggered.connect(self.setting24Hr)
        self.ui.actionShow_Seconds.triggered.connect(self.settingSecs)
        self.ui.actionShow_Date.triggered.connect(self.settingDate)
        self.ui.actionShow_AM_PM.triggered.connect(self.settingHr12Notation)
        self.ui.action_Exit.triggered.connect(self.close)
        self.ui.actionDark_Mode.triggered.connect(self.settingDarkMode)
        self.ui.actionIncrease_Font.triggered.connect(self.settingIncreaseFont)
        self.ui.actionDecrease_Font.triggered.connect(self.settingDecreaseFont)
        self.ui.actionFrameless.triggered.connect(self.settingFramelessWindowBar)
        self.ui.actionUse_Native_Theme.triggered.connect(self.settingUseNativeTheme)

    def getTime(self):
        dt = datetime.datetime.now()

        # Update Time
        if self.json.return_specific_json("is24Hr") is True:  # 24 Hr
            self.ui.Hour.setText(dt.strftime("%H"))
            self.ui.hr12Notation.setText("")

        else:  # 12 Hr
            self.ui.Hour.setText(dt.strftime("%I"))
            if self.json.return_specific_json("showHr12") is True:  # Show AM/PM
                self.ui.hr12Notation.setText(dt.strftime("%p"))

            else:
                self.ui.hr12Notation.setText("")

        self.ui.Mins.setText(dt.strftime("%M"))
        self.ui.Secs.setText(dt.strftime("%S"))

        if self.json.return_specific_json("showSecs") is True:  # Show Secs
            self.ui.Secs.setVisible(True)
            self.ui.Sep2.setVisible(True)

        else:
            self.ui.Secs.setVisible(False)
            self.ui.Sep2.setVisible(False)

        # Update Date
        self.ui.DayName.setText(dt.strftime('%A'))
        self.ui.Date.setText(f"{dt.day} {dt.strftime('%B')} {dt.year}")
        self.ui.DateSep.setText(",")

        if self.json.return_specific_json("showDate") is True:
            self.ui.DayName.setVisible(True)
            self.ui.Date.setVisible(True)
            self.ui.DateSep.setVisible(True)
            self.ui.line.setVisible(True)

        else:
            self.ui.DayName.setVisible(False)
            self.ui.Date.setVisible(False)
            self.ui.DateSep.setVisible(False)
            self.ui.line.setVisible(False)

        # Update Font
        if self.json.return_specific_json("fontType") is not None:
            time_font = QFont(
                self.json.return_specific_json("fontType"), self.json.return_specific_json("fontSizeTime")
            )
            hr12notation_font = QFont(
                self.json.return_specific_json("fontType"), self.json.return_specific_json("fontSize12Hr")
                if self.json.return_specific_json("fontSize12Hr") <= self.json.return_specific_json("fontSizeTime")
                else self.json.return_specific_json("fontSizeTime"))
            date_font = QFont(
                self.json.return_specific_json("fontType"), self.json.return_specific_json("fontSizeDate")
            )

            self.ui.Hour.setFont(time_font)
            self.ui.Mins.setFont(time_font)
            self.ui.Secs.setFont(time_font)
            self.ui.Sep1.setFont(time_font)
            self.ui.Sep2.setFont(time_font)

            self.ui.hr12Notation.setFont(hr12notation_font)

            self.ui.Date.setFont(date_font)
            self.ui.DateSep.setFont(date_font)
            self.ui.DayName.setFont(date_font)

    def openSettings(self):
        settings_ui = TimeDisplaySettings(parent=self)
        settings_ui.setWindowTitle("Settings")
        settings_ui.exec()
        self.json.getConfigData()  # Re-formulate JSON after settings change
        self.runSettings()  # Update GUI based on formulated settings change

    def updateSettingState(self):
        self.ui.action_Float_on_Top.setChecked(self.json.return_specific_json("isFloating"))
        self.ui.actionUse_24_Hour_Format.setChecked(self.json.return_specific_json("is24Hr"))
        self.ui.actionShow_Seconds.setChecked(self.json.return_specific_json("showSecs"))
        self.ui.actionShow_Date.setChecked(self.json.return_specific_json("showDate"))
        self.ui.actionShow_AM_PM.setChecked(self.json.return_specific_json("showHr12"))
        self.ui.actionDark_Mode.setChecked(self.json.return_specific_json("darkMode"))
        self.ui.actionFrameless.setChecked(self.json.return_specific_json("framelessWindowBar"))
        self.ui.actionUse_Native_Theme.setChecked(self.json.return_specific_json("useNativeTheme"))

    def onFloatChange(self):
        if self.json.return_specific_json("isFloating") is True:
            self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        else:
            self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, False)

        # Refresh Window
        self.show()

    def runSettings(self):
        self.onSwitchTheme()
        self.onFloatChange()
        self.onUpdateWinVisibility()
        self.onUpdateWindowBar()

    def settingFloat(self):
        self.json.update_specific_json("isFloating", self.ui.action_Float_on_Top.isChecked())
        self.json.update_json_file()
        return self.onFloatChange()

    def setting24Hr(self):
        self.json.update_specific_json("is24Hr", self.ui.actionUse_24_Hour_Format.isChecked())
        self.json.update_json_file()

    def settingSecs(self):
        self.json.update_specific_json("showSecs", self.ui.actionShow_Seconds.isChecked())
        self.json.update_json_file()

    def settingDate(self):
        self.json.update_specific_json("showDate", self.ui.actionShow_Date.isChecked())
        self.json.update_json_file()

    def settingHr12Notation(self):
        self.json.update_specific_json("showHr12", self.ui.actionShow_AM_PM.isChecked())
        self.json.update_json_file()

    def settingDarkMode(self):
        self.json.update_specific_json("darkMode", self.ui.actionDark_Mode.isChecked())
        self.json.update_json_file()
        return self.onSwitchTheme()

    def settingUseNativeTheme(self):
        self.json.update_specific_json("useNativeTheme", self.ui.actionUse_Native_Theme.isChecked())
        self.json.update_json_file()
        return self.onSwitchTheme()

    def settingFramelessWindowBar(self):
        self.json.update_specific_json("framelessWindowBar", self.ui.actionFrameless.isChecked())
        self.json.update_json_file()
        return self.onUpdateWindowBar()

    def settingIncreaseFont(self):
        self.json.update_specific_json("fontSizeTime", self.json.return_specific_json("fontSizeTime") + 1)
        self.json.update_specific_json("fontSizeDate", self.json.return_specific_json("fontSizeDate") + 1)
        self.json.update_specific_json("fontSize12Hr", self.json.return_specific_json("fontSize12Hr") + 1)
        self.json.update_json_file()

    def settingDecreaseFont(self):
        self.json.update_specific_json("fontSizeTime", self.json.return_specific_json("fontSizeTime") - 1)
        self.json.update_specific_json("fontSizeDate", self.json.return_specific_json("fontSizeDate") - 1)
        self.json.update_specific_json("fontSize12Hr", self.json.return_specific_json("fontSize12Hr") - 1)
        self.json.update_json_file()

    def resizeEvent(self, a0: QResizeEvent):
        super().resizeEvent(a0)
        size = self.size()
        self.json.update_specific_json("memHWindowSize", size.width())
        self.json.update_specific_json("memVWindowSize", size.height())
        self.json.update_json_file()

    def initResize(self):
        size = QSize()
        size.setWidth(self.json.return_specific_json("memHWindowSize"))
        size.setHeight(self.json.return_specific_json("memVWindowSize"))

        print(size)

        self.resize(size)

    def onSwitchTheme(self):
        if self.json.return_specific_json("useNativeTheme"):
            self.setStyleSheet(None)
        elif self.json.return_specific_json("darkMode"):
            self.setStyleSheet(QT_STYLESHEET_DARK)
        else:
            self.setStyleSheet(QT_STYLESHEET_LIGHT)

    def onUpdateWinVisibility(self):
        self.setWindowOpacity(self.json.return_specific_json("windowVisibility")/100)
        self.show()

    def onUpdateWindowBar(self):
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, self.json.return_specific_json("framelessWindowBar"))
        self.show()


class TimeDisplaySettings(QDialog):
    def __init__(self, parent=None):
        super(TimeDisplaySettings, self).__init__(parent)
        self.ui = Ui_Settings()
        self.json = ConfigJSON(CONFIG_NAME)
        self.json.generate_config()
        self.json.getConfigData()

        # Setup UI
        self.ui.setupUi(self)
        self.onSwitchTheme()
        self.onUpdateFont()

        # Setup Config States
        if self.json.return_specific_json("fontType") is not None:
            self.ui.FontUsage.setCurrentFont(QFont(self.json.return_specific_json("fontType")))
        self.ui.TimeSize.setValue(self.json.return_specific_json("fontSizeTime"))
        self.ui.DateSize.setValue(self.json.return_specific_json("fontSizeDate"))
        self.ui.Hr12NotationSize.setValue(self.json.return_specific_json("fontSize12Hr"))
        self.ui.hr24Usage.setChecked(self.json.return_specific_json("is24Hr"))
        self.ui.FloatWindow.setChecked(self.json.return_specific_json("isFloating"))
        self.ui.Hr12NotUsage.setChecked(self.json.return_specific_json("showHr12"))
        self.ui.ShowSeconds.setChecked(self.json.return_specific_json("showSecs"))
        self.ui.ShowDate.setChecked(self.json.return_specific_json("showDate"))
        self.ui.useDarkMode.setChecked(self.json.return_specific_json("darkMode"))
        self.ui.WindowVisibilitySlider.setValue(self.json.return_specific_json("windowVisibility"))
        self.ui.setFrameless.setChecked(self.json.return_specific_json("framelessWindowBar"))
        self.ui.setUseNativeTheme.setChecked(self.json.return_specific_json("useNativeTheme"))

        # Font
        if self.json.return_specific_json("fontType") is not None:
            font = QFont(self.json.return_specific_json("fontType"), 20)
            title_font = QFont(self.json.return_specific_json("fontType"), 30)
            self.ui.TimeSize.setFont(font)
            self.ui.DateSize.setFont(font)
            self.ui.Hr12NotUsage.setFont(font)
            self.ui.FloatWindow.setFont(font)
            self.ui.FontLabel.setFont(font)
            self.ui.hr24Usage.setFont(font)
            self.ui.TimeSizeLabel.setFont(font)
            self.ui.DateSizeLabel.setFont(font)
            self.ui.Hr12NotationSizeLabel.setFont(font)
            self.ui.FontUsage.setFont(font)
            self.ui.Hr12NotationSize.setFont(font)
            self.ui.ShowSeconds.setFont(font)
            self.ui.ShowDate.setFont(font)
            self.ui.useDarkMode.setFont(font)
            self.ui.WindowVisibilitySlider.setFont(font)
            self.ui.setFrameless.setFont(font)
            self.ui.setUseNativeTheme.setFont(font)
            self.ui.label.setFont(title_font)

    def accept(self):
        # Update Values
        self.json.update_specific_json("fontType", self.ui.FontUsage.currentText())
        self.json.update_specific_json("fontSizeTime", self.ui.TimeSize.value())
        self.json.update_specific_json("fontSizeDate", self.ui.DateSize.value())
        self.json.update_specific_json("fontSize12Hr", self.ui.Hr12NotationSize.value())
        self.json.update_specific_json("is24Hr", self.ui.hr24Usage.isChecked())
        self.json.update_specific_json("isFloating", self.ui.FloatWindow.isChecked())
        self.json.update_specific_json("showHr12", self.ui.Hr12NotUsage.isChecked())
        self.json.update_specific_json("showSecs", self.ui.ShowSeconds.isChecked())
        self.json.update_specific_json("showDate", self.ui.ShowDate.isChecked())
        self.json.update_specific_json("darkMode", self.ui.useDarkMode.isChecked())
        self.json.update_specific_json("windowVisibility", self.ui.WindowVisibilitySlider.value())
        self.json.update_specific_json("framelessWindowBar", self.ui.setFrameless.isChecked())
        self.json.update_specific_json("useNativeTheme", self.ui.setUseNativeTheme.isChecked())

        # Update JSON File
        self.json.update_json_file()

        # Update UI
        self.onSwitchTheme()
        self.onUpdateFont()

        # Close UI
        self.close()

    def onSwitchTheme(self):
        if self.json.return_specific_json("useNativeTheme"):
            self.setStyleSheet(None)
        elif self.json.return_specific_json("darkMode") is True:
            self.setStyleSheet(QT_STYLESHEET_DARK)
        else:
            self.setStyleSheet(QT_STYLESHEET_LIGHT)

    def onUpdateFont(self):
        if self.json.return_specific_json("fontType") is not None:
            font = QFont(self.json.return_specific_json("fontType"), 20)
            title_font = QFont(self.json.return_specific_json("fontType"), 30)
            self.ui.TimeSize.setFont(font)
            self.ui.DateSize.setFont(font)
            self.ui.Hr12NotUsage.setFont(font)
            self.ui.FloatWindow.setFont(font)
            self.ui.FontLabel.setFont(font)
            self.ui.hr24Usage.setFont(font)
            self.ui.TimeSizeLabel.setFont(font)
            self.ui.DateSizeLabel.setFont(font)
            self.ui.Hr12NotationSizeLabel.setFont(font)
            self.ui.FontUsage.setFont(font)
            self.ui.Hr12NotationSize.setFont(font)
            self.ui.ShowSeconds.setFont(font)
            self.ui.ShowDate.setFont(font)
            self.ui.useDarkMode.setFont(font)
            self.ui.WindowVisibilityLabel.setFont(font)
            self.ui.setFrameless.setFont(font)
            self.ui.setUseNativeTheme.setFont(font)
            self.ui.label.setFont(title_font)


def run_GUI():
    """
    Run the Graphical User Interface of the Application.
    :return:
    """
    td_app = QApplication(sys.argv)
    td = TimeDisplayGUI()
    # td.show()
    sys.exit(td_app.exec())
