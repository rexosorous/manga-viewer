# standard libraries
import os
import sys

# dependencies
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# local modules
import reader
import home

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
app = QApplication(sys.argv)
# window = reader.Reader()
window = home.Home()
window.showMaximized()
sys.exit(app.exec())