# dependencies
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QObject



class Signals(QObject):
    """Holds all the signals to be emitted and connected.

    Note:
        These signals must be class attributes and an instance of this class must be created for the signals to work

    Attributes:
        open_book_signal (pyqtSignal): emitted when a book spine is double clicked to open the reader
        close_book_signal (pyqtSignal): emitted when a book is closed in the reader to open up the library
        update_metadata (pyqtSignal): emitted when changes are made to the metadata to update all metadata lists
    """
    open_book_signal = pyqtSignal(str)
    close_book_signal = pyqtSignal()
    filter_signal = pyqtSignal(str)
    update_metadata = pyqtSignal()
    update_spines = pyqtSignal()