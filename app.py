# standard libraries
import os
import sys

# dependencies
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# local modules
import home
import constants as const
import signals


QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
app = QApplication(sys.argv)

sigs = signals.Signals()

home_window = home.Home(sigs, const.directory)
home_window.showMaximized()

sys.exit(app.exec())