# standard libraries
import os
import sys

# dependencies
from PyQt5.QtWidgets import QApplication, QStackedWidget
from PyQt5.QtCore import Qt

# local modules
import reader
import home
import constants as const


QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
app = QApplication(sys.argv)

home_window = home.Home(const.directory)
home_window.showMaximized()
reader_window = reader.Reader()

stack = QStackedWidget()
stack.addWidget(home_window)
stack.addWidget(reader_window)
stack.setWindowTitle("Manga Viewer")

def open_reader(book: str):
    reader_window.open_book(book)
    stack.setCurrentIndex(1)
def close_reader():
    stack.setCurrentIndex(0)
home_window.open_book_signal.connect(open_reader)
reader_window.close_book_signal.connect(close_reader)

stack.setPalette(const.background_color)


stack.showMaximized()

sys.exit(app.exec())