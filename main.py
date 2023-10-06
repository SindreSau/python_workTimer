import configparser

from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar, QVBoxLayout
import sys
from appcontent import AppContent
from colors import Colors


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Get config
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.configUiZoom = float(self.config['APP_SETTINGS']['uiZoom'])

        self.setWindowTitle('Countdown')
        self.setFixedSize(int(400 * self.configUiZoom), int(500 * self.configUiZoom))
        self.setCentralWidget(AppContent(self))

        # Appcontent
        self.appcontent = AppContent(self)
        self.setCentralWidget(self.appcontent)
        self.appcontent.setStyleSheet(f'background-color: {Colors.titlebar};')


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication([])
    app.setApplicationName('Countdown')
    app.setApplicationVersion('0.1')

    # Create a window
    window = MainWindow()
    window.setStyleSheet(f'background-color: {Colors.background}')
    window.show()

    # Start the event loop.
    app.exec_()
