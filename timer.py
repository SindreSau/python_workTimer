from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from pygame import mixer
from colors import Colors


class Timer(QWidget):
    def __init__(self, parent=None, worktime=45, breaktime=15):
        super().__init__(parent)
        # Variables
        self.timer = None
        self.parent = parent
        self.worktime = worktime
        self.breaktime = breaktime
        self.work = True

        # From config
        self.config = self.parent.config
        self.configUiZoom = float(self.config['APP_SETTINGS']['uiZoom'])

        # Main layout
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.layout)

        # BACK TO START BUTTON
        self.backButton = QPushButton(QIcon('icons/back.png'), '', self)
        self.backButton.setFixedSize(40, 40)
        self.backButton.setIconSize(QSize(20, 20))
        self.backButton.setStyleSheet(
            "QPushButton {"
            "border-radius: 5px; "
            "padding: 2px;"
            "}"
            "QPushButton:hover {"
            f"background-color: {Colors.titlebar}; "
            "}"
            "QPushButton:hover:pressed {"
            f"background-color: {Colors.background}; "
            "}"
            "QPushButton:focus {"
            f"border-color: {Colors.titlebar}; "
            "}"
        )
        self.backButton.clicked.connect(self.parent.backToStart)

        # SUBLAYOUT FOR WORK OR BREAK AND NUMBERDISPLAY
        self.subLayout = QVBoxLayout()
        self.subLayout.setSpacing(10)
        self.subLayout.setContentsMargins(50, 0, 50, 0)
        self.subLayout.setAlignment(Qt.AlignCenter)

        # WORK OR BREAK
        self.workOrBreak = QLabel(f'{"Work" if self.work else "Break"}')
        self.workOrBreak.setStyleSheet(
            f'color: {Colors.text};'
            'font-size: 20px;'
            'font-weight: bold;'
        )
        self.workOrBreak.setAlignment(Qt.AlignCenter)

        # NUMBERDISPLAY
        self.numberDisplay = QLabel()
        self.numberDisplay.setStyleSheet(
            f'color: {Colors.text};'
            'font-size: 80px;'
            'font-weight: bold;'
        )
        self.numberDisplay.setAlignment(Qt.AlignCenter)

        # ADD TO LAYOUT
        self.layout.addWidget(self.backButton)
        self.subLayout.addWidget(self.workOrBreak)
        self.subLayout.addWidget(self.numberDisplay)
        self.layout.addLayout(self.subLayout)

    def setStartTime(self, worktime, breaktime):
        self.worktime = worktime
        self.breaktime = breaktime

    # TIMER LOGIC
    def run(self, work=True):
        work = work
        self.workOrBreak.setText(f'{"Work" if work else "Break"}')
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateTimer)

        if work:
            self.seconds = self.worktime * 60
            self.displayTime(self.formatSeconds(self.seconds))
        else:
            self.seconds = self.breaktime * 60
            self.displayTime(self.formatSeconds(self.seconds))

        self.timer.start(1000)

    def updateTimer(self):
        self.seconds -= 10
        self.displayTime(self.formatSeconds(self.seconds))
        if self.seconds == 0:
            self.timer.stop()
            if self.work:
                self.run(False)
                self.work = False
                mixer.init()
                mixer.music.load("audio/montbell-bonsho-von-japan-30695.mp3")
                mixer.music.play()
            else:
                self.run()
                self.work = True
                mixer.init()
                mixer.music.load("audio/clock-alarm-8761.mp3")
                mixer.music.play()

    def formatSeconds(self, seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f'{minutes:02}:{seconds:02}'

    def displayTime(self, timeAsString):
        self.numberDisplay.setText(timeAsString)
