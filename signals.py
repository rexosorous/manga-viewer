# dependencies
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal



class Signals(QObject):
    update_metadata = pyqtSignal()