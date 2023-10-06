import time

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox, QLineEdit

from colors import Colors


class Settings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Variables
        self.parent = parent

        # Config file
        self.config = self.parent.config
        self.configUiZoom = float(self.config['APP_SETTINGS']['uiZoom'])

        # Layout
        self.layout = QVBoxLayout()
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(int(80 * self.configUiZoom), 50, int(80 * self.configUiZoom), 50)
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

        # ZOOMPICKER
        self.zoomPicker = QComboBox()
        self.zoomPicker.setStyleSheet(
            "QComboBox {"
            "border-radius: 3px; "
            "border-style: outset; "
            "border-width: 1px; "
            "padding: 5px;"
            f"border-color: {Colors.titlebar}; "
            "}"
            "QComboBox:focus {"
            "border-color: #52CC99; "
            "}"
        )

        # Add items
        self.zoomPicker.addItem('100%')
        self.zoomPicker.addItem('125%')

        # Set current zoom
        if self.configUiZoom == 1.0:
            self.zoomPicker.setCurrentIndex(0)
        elif self.configUiZoom == 1.25:
            self.zoomPicker.setCurrentIndex(1)

        # zoomPicker handling
        self.zoomPicker.activated[str].connect(self.parent.updateUiZoom)

        # WORKTIME
        self.worktimeEdit = QLineEdit()
        self.worktimeEdit.setPlaceholderText('Worktime')
        self.worktimeEdit.setStyleSheet(
            "QLineEdit {"
            "border-radius: 3px; "
            "border-style: outset; "
            "border-width: 1px; "
            "padding: 5px;"
            f"border-color: {Colors.titlebar}; "
            "}"
            "QLineEdit:focus {"
            "border-color: #52CC99; "
            "}"
        )

        # Set current worktime
        self.worktimeEdit.setText(self.config['APP_SETTINGS']['worktime'])

        # BREAKTIME
        self.breaktimeEdit = QLineEdit()
        self.breaktimeEdit.setPlaceholderText('Breaktime')
        self.breaktimeEdit.setStyleSheet(
            "QLineEdit {"
            "border-radius: 3px; "
            "border-style: outset; "
            "border-width: 1px; "
            "padding: 5px;"
            f"border-color: {Colors.titlebar}; "
            "}"
            "QLineEdit:focus {"
            "border-color: #52CC99; "
            "}"
        )

        # Set current breaktime
        self.breaktimeEdit.setText(self.config['APP_SETTINGS']['breaktime'])

        # SAVEBUTTON
        self.saveButton = QPushButton('Save')
        self.saveButton.setStyleSheet(
            "QPushButton {"
            "border-radius: 3px; "
            "border-style: outset; "
            "border-width: 1px; "
            "padding: 8px;"
            f"border-color: {Colors.titlebar}; "
            "}"
            "QPushButton:hover {"
            f"background-color: {Colors.titlebar}; "
            "}"
            "QPushButton:hover:pressed {"
            f"background-color: {Colors.background}; "
            "}"
            "QPushButton:focus {"
            "border-color: #52CC99; "
            "}"
        )

        # Savebutton handling
        self.saveButton.clicked.connect(lambda: self.parent.saveSettings(self.worktimeEdit.text(), self.breaktimeEdit.text()))

        # Add to layout
        self.layout.addWidget(self.zoomPicker)
        self.layout.addWidget(self.worktimeEdit)
        self.layout.addWidget(self.breaktimeEdit)
        self.layout.addWidget(self.saveButton)

    def alertSaved(self):
        self.saveButton.setText('Saved!')
        self.saveButton.setDisabled(True)

        timer = QTimer
        timer.singleShot(800, self.resetSaveButton)

    def alertError(self):
        self.saveButton.setText('Invalid settings')
        self.saveButton.setDisabled(True)

        timer = QTimer
        timer.singleShot(800, self.resetSaveButton)

    def resetSaveButton(self):
        self.saveButton.setText('Save')
        self.saveButton.setDisabled(False)