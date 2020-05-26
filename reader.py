# standard libraries
from os import listdir

# dependencies
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

# local modules
from reader_window import Ui_MainWindow




"""
TODO
    * connect back and edit buttons
    * connect 'esc' key to same func as back button
    * populate page_list and allow clicking to jump pages
    * populate series_list and allow clicking to jump books
"""


class Reader(QtWidgets.QMainWindow, Ui_MainWindow):
    """Window used to read pages in the manga

    Attributes:
        image (QLabel): label used to load pixmaps onto
        page_counter (QLabel): shows the current page. should be 'Page x/y'
        back_button (QPushButton): goes back to the main window
        edit_button (QPushButton): edits the current book's metadata
        page_list (QListWidget): shows all pages, allowing the user to select one to jump to
        series_list (QListWidget): shows all books in the series, allowing the user to jump to a sequel or prequel
        pages ([str]): holds filenames for each page in the book
        current_page (int): the page of the book currently being viewed. 0 for the first page
        size (float): size multiplier. ex: 1 means 100%, 1.1 means 110%, 0.9 means 90%
    """
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # init attributes
        self.pages = self.get_imgs()
        self.current_page = 0
        self.size = 1

        # change displayed images/text
        self.page_counter.setText(f'Page {self.current_page+1}/{len(self.pages)}')
        self.draw()

        # add hotkeys
        QtWidgets.QShortcut(Qt.Key_Right, self, self.next_page)
        QtWidgets.QShortcut(Qt.Key_Left, self, self.prev_page)
        QtWidgets.QShortcut(Qt.Key_Equal, self, self.zoom_in)
        QtWidgets.QShortcut(Qt.Key_Minus, self, self.zoom_out)



    def next_page(self):
        """Displays the next page in the book

        Triggered by right arrow key
        """
        self.current_page += 1
        if self.current_page >= len(self.pages): # prevent index out of range error
            self.current_page = len(self.pages) - 1
        self.draw()



    def prev_page(self):
        """Displays the previous page in the book

        Triggered by left arrow key
        """
        self.current_page -= 1
        if self.current_page <= 0: # prevent index out of range error
            self.current_page = 0
        self.draw()



    def zoom_in(self):
        """Zooms the page in by 5%

        Triggered by =/+
        """
        self.size += 0.05
        self.draw()



    def zoom_out(self):
        """Zooms out the page by 5%

        Triggered by -/_
        """
        self.size -= 0.05
        if self.size < 0.05: # don't let users zoom out to below 5% of the original picture size
            self.size = 0.05
        self.draw()



    def get_imgs(self) -> [str]:
        """Gets a list of all image files in a folder

        Returns:
            [str]: a relative directory for each file
        """
        return [f'jojo/{x}' for x in listdir('jojo/')]



    def draw(self):
        """Displays a page in the book

        Also resizes the image, sets the page_counter text, and moves the scrollbar back to the top
        """
        pixmap = QPixmap(self.pages[self.current_page])
        pixmap = pixmap.scaled(int(pixmap.width()*self.size), int(pixmap.height()*self.size), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image.setPixmap(pixmap)
        self.page_counter.setText(f'Page {self.current_page+1}/{len(self.pages)}')
        self.scrollArea.verticalScrollBar().setSliderPosition(0)