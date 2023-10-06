from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel


class StartTimer(QWidget):
    def __init__(self, parent=None, worktime=45, breaktime=15):
        super().__init__(parent)
        self.parent = parent
        self.worktime = worktime
        self.breaktime = breaktime

        # Layout
        self.layout = QVBoxLayout()
        self.layout.setSpacing(50)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)

        # Play button
        self.buttonLayout = QVBoxLayout()
        self.buttonLayout.setSpacing(0)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout.setAlignment(Qt.AlignCenter) # Center button
        self.layout.addLayout(self.buttonLayout)

        self.playIcon = QIcon("icons/play.png")
        self.playButton = QPushButton(
            self.playIcon,
            "",
            self
        )
        self.playButton.setIconSize(QSize(80, 80))
        self.playButton.setFixedSize(120, 120)
        self.playButton.setStyleSheet(
            "QPushButton {"
            "border-radius: 60px; "
            "border-style: outset; "
            "border-width: 1px; "
            "border-color: #202020; "
            "padding-left: 10px;"  # Nudge the icon 10 pixels to the right
            "}"
            "QPushButton:hover {"
            "background-color: #202020; "
            "}"
            "QPushButton:hover:pressed {"
            "background-color: #52CC99; "
            "}"
            "QPushButton:focus {"
            "border-color: #52CC99; "
            "}"
        )
        self.playButton.clicked.connect(self.parent.startTimer)
        self.layout.addWidget(self.playButton)

        self.buttonLayout.addWidget(self.playButton)

        # Info text
        self.textLayout = QVBoxLayout()
        self.textLayout.setSpacing(10)
        self.textLayout.setContentsMargins(0, 0, 0, 0)

        # Heading
        self.infoText = QLabel('Current settings')
        self.infoText.setWordWrap(True)
        self.infoText.setStyleSheet('color: #7a7a7a; font-size: 22px')

        # Work time
        self.infoTextWork = QLabel(f'Work: {self.worktime}')
        self.infoTextWork.setWordWrap(True)
        self.infoTextWork.setStyleSheet('color: #4a4a4a; font-size: 18px')

        # Break time
        self.infoTextBreak = QLabel(f'Break: {self.breaktime}')
        self.infoTextBreak.setWordWrap(True)
        self.infoTextBreak.setStyleSheet('color: #4a4a4a; font-size: 18px')

        self.textLayout.addWidget(self.infoText)
        self.textLayout.addWidget(self.infoTextWork)
        self.textLayout.addWidget(self.infoTextBreak)
        self.layout.addLayout(self.textLayout)

    def setStartTime(self, worktime, breaktime):
        self.worktime = worktime
        self.breaktime = breaktime
        self.infoTextWork.setText(f'Work: {worktime}')
        self.infoTextBreak.setText(f'Break: {breaktime}')

    def setFocusToPlayButton(self):
        self.playButton.setFocus()