# standard libraries
import os
import sys

# dependencies
from PyQt5.QtWidgets import QApplication

# local modules
import reader

app = QApplication(sys.argv)
window = reader.Reader()
window.show()
sys.exit(app.exec())