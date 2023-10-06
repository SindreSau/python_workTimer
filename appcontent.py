import configparser

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QPushButton, QSpacerItem, QHBoxLayout, \
    QStackedWidget
from PyQt5.QtCore import Qt
from RoundProgressBar import QRoundProgressBar
from settings import Settings
from colors import Colors
from startTimer import StartTimer
from timer import Timer


def resetSettings():
    # Create config file
    config = configparser.ConfigParser()
    config['APP_SETTINGS'] = {
        'worktime': '45',
        'breaktime': '15',
        'uiZoom': '1.0'
    }
    with open('config.ini', 'w') as configfile:
        config.write(configfile)


class AppContent(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.isSettingsOpen = False

        # Config file
        self.config = self.parent.config
        self.configUiZoom = float(self.config['APP_SETTINGS']['uiZoom'])
        self.workTime = int(self.config['APP_SETTINGS']['worktime'])
        self.breakTime = int(self.config['APP_SETTINGS']['breaktime'])

        # Layout
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # Titlebar with settings icon on right
        self.titlebar = QWidget()
        self.titlebar_layout = QHBoxLayout()
        self.titlebar_layout.setContentsMargins(0, 0, 0, 0)
        self.titlebar.setLayout(self.titlebar_layout)
        self.titlebar.setStyleSheet('background-color: #202020;')
        self.titlebar.setFixedHeight(50)
        self.titlebar_layout.setContentsMargins(10, 0, 10, 0)
        self.layout.addWidget(self.titlebar)
        self.layout.setStretchFactor(self.titlebar, 0)
        self.layout.setAlignment(self.titlebar, Qt.AlignTop)

        # Titlebar content
        self.titlebar_title = QLabel('Work your ass off')
        self.titlebar_title.setStyleSheet(f'color: {Colors.primary}; font-size: 20px')

        self.titlebar_settings = QPushButton(
            QIcon("icons/setting.png"),
            "",
            self
        )
        self.titlebar_settings.setFixedSize(40, 40)
        self.titlebar_settings.setStyleSheet(
            "QPushButton {"
            "border-radius: 5px; "
            "border-style: outset; "
            "border-width: 1px; "
            f"border-color: {Colors.background}; "
            "}"
            "QPushButton:hover {"
            f"background-color: {Colors.background}; "
            "}"
            "QPushButton:hover:pressed {"
            f"background-color: {Colors.titlebar}; "
            "}"
            "QPushButton:focus {"
            "border-color: #52CC99; "
            "}"
        )
        self.titlebar_settings.setShortcut("Ctrl+,")
        self.titlebar_settings.clicked.connect(self.toggleSettings)

        # Add title and settings to titlebar
        self.titlebar_layout.addWidget(self.titlebar_title)
        self.titlebar_layout.addWidget(self.titlebar_settings)

        # Main content layout
        self.main_content = QStackedWidget()
        self.main_content.setStyleSheet(f'background-color: {Colors.background};')
        self.layout.addWidget(self.main_content)
        self.layout.setStretchFactor(self.main_content, 10)

        # Settings content
        self.settings = Settings(self)
        self.main_content.addWidget(self.settings)

        # start content
        self.start = StartTimer(self, self.workTime, self.breakTime)
        self.main_content.addWidget(self.start)
        self.main_content.setCurrentWidget(self.start)
        self.start.setFocusToPlayButton() # Set focus to play button on launch
        self.currentMainContent = self.start

        # Timer content
        self.timer = Timer(self, self.workTime, self.breakTime)
        self.main_content.addWidget(self.timer)

    def toggleSettings(self):
        self.isSettingsOpen = not self.isSettingsOpen
        self.titlebar_settings.setShortcut('Esc' if self.isSettingsOpen else 'Ctrl+,')
        self.titlebar_settings.setIcon(QIcon("icons/close.png") if self.isSettingsOpen else QIcon("icons/setting.png"))

        if self.isSettingsOpen:
            self.main_content.addWidget(self.settings)
            self.main_content.setCurrentWidget(self.settings)
        else:
            self.main_content.removeWidget(self.settings)
            self.main_content.setCurrentWidget(self.currentMainContent)

    def startTimer(self):
        self.timer.run()
        self.main_content.setCurrentWidget(self.timer)
        self.currentMainContent = self.timer

    def updateUiZoom(self, zoom):
        self.configUiZoom = float(zoom[:-1]) / 100
        self.config['APP_SETTINGS']['uiZoom'] = str(self.configUiZoom)
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)
        self.parent.setFixedSize(int(400 * self.configUiZoom), int(500 * self.configUiZoom))

    def saveSettings(self, worktime, breaktime):
        # Errorhandling
        worktime = int(worktime)
        breaktime = int(breaktime)

        if worktime > 0 and breaktime > 0:
            self.config['APP_SETTINGS']['worktime'] = str(worktime)
            with open('config.ini', 'w') as configfile:
                self.config.write(configfile)

            self.config['APP_SETTINGS']['breaktime'] = str(breaktime)
            with open('config.ini', 'w') as configfile:
                self.config.write(configfile)

            # Update start content
            self.start.setStartTime(worktime, breaktime)
            self.timer.setStartTime(worktime, breaktime)

            self.settings.alertSaved()
        else:
            self.settings.alertError()

    def backToStart(self):
        self.main_content.setCurrentWidget(self.start)
        self.currentMainContent = self.start
        self.start.setFocusToPlayButton()

