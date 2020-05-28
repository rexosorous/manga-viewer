# standard libraries
from functools import partial
from os import listdir
import random

# dependencies
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMenu
from PyQt5 import QtCore

# local modules
from ui.main_window import Ui_MainWindow
import spines
import constants as const




"""
TODO
    * implement search bar functionality
    * implement sorting
    * write logic for side panel (editing book details and search filter)
"""

class Home(QMainWindow, Ui_MainWindow):
    """Window used to read pages in the manga

    Attributes:
        search_bar (QLineEdit)
        search_button (QPushButton): same function as pressing entet in search bar
        adv_search_button (QPushButton): opens a new window with all searchable options
        sort_by (QComboBox): contains "Alphabetically", "Rating", and "Randomly"
        random_button (QPushButton): randomly selects from the list

        bookshelf (QGridLayout): the layout where all the books will be displayed
        bookshelf_area (QScrollArea): the whole area where books will be displayed

        side_header (QLabel):
        side_img (QLabel):
        side_help (QTextBrowser):
        side_title_text (QLineEdit):
        side_artist_text (QLineEdit):
        side_artist_dropdown (QComboBox):
        side_artist_list (QListWidget):
        side_collection_text (QLineEdit):
        side_collection_dropdown (QComboBox):
        side_order_number (QSpinBox): >= 0
        side_rating_number (QSpinBox): 0 <= x <= 10
        side_rating_toggle (QCheckBox): include higher ratings if checked else only this rating
        side_genre_text (QLineEdit):
        side_genre_dropdown (QComboBox):
        side_genre_list (QListWidget):
        side_tags_list (QLineEdit):
        side_tags_dropdown (QComboBox):
        side_tags_list (QListWidget):

        open_book_signal (pyqtSignal): triggered to open a book to read
        books ([QFrame]): holds a list of all book frames
        selected ([QFrame]): holds all currently selected books
    """
    open_book_signal = QtCore.pyqtSignal(str)

    def __init__(self, directory):
        super().__init__()
        self.setupUi(self)

        # init attributes
        self.directory = directory
        self.books = []
        self.selected = []

        # set up ui
        self.side_help.setVisible(False)

        self.connect_signals()
        self.generate_books()
        self.populate()



    def connect_signals(self):
        """Connects each signal to their respective functions
        """
        self.adv_search_button.clicked.connect(self.toggle_side_panel)
        self.sort_by.currentIndexChanged.connect(self.populate)
        self.random_button.clicked.connect(self.random_select)
        self.bookshelf_area.contextMenuEvent = self.context_menu
        self.bookshelf_area.mousePressEvent = self.reset_selected
        self.bookshelf_area.keyPressEvent = self.keyboard_handler



    def toggle_side_panel(self):
        """Switches the side panel from details to advanced search and vice-versa

        Note:
            Most elements stay the same in both
        """
        if self.side_img.isVisible():
            # switch to filter
            self.side_img.setVisible(False)
            self.side_help.setVisible(True)
            self.side_header.setText('Advanced Search')
            self.side_submit_button.setText('Filter')
        else:
            # switch to details
            self.side_help.setVisible(False)
            self.side_img.setVisible(True)
            self.side_header.setText('Details')
            self.side_submit_button.setText('Submit Changes')



    def random_select(self):
        """Randomly selects a book from the list
        """
        self.reset_selected()
        choice = random.choice(self.books)
        self.highlight(choice)
        self.selected = [choice]



    def keyboard_handler(self, event):
        """Unhighlights a book in the gallery when the mouse leaves the area

        Args:
            event (QKeyEvent): The event that was emitted
        """
        if event.key() == QtCore.Qt.Key_A and event.modifiers() == QtCore.Qt.ControlModifier: # control + a
            # select all books
            for book in self.books:
                self.selected.append(book) if book not in self.selected else None
                self.highlight(book)

        # arrow key navigation
        # elif event.key() == QtCore.Qt.Key_Up:
        # elif event.key() == QtCore.Qt.Key_Right:
        # elif event.key() == QtCore.Qt.Key_Down:
        # elif event.key() == QtCore.Qt.Key_Left:




    def generate_books(self):
        """Creates objects for the books
        """
        for book in listdir(f'{self.directory}/'):
            # set up frame
            spine = spines.BookSpine(book, self.directory)

            # add the new frames to the list
            self.books.append(spine)

            # connect events
            spine.mousePressEvent = partial(self.select, self.books[-1])
            spine.mouseDoubleClickEvent = partial(self.open_book, self.books[-1])
            spine.enterEvent = partial(self.highlight, self.books[-1])
            spine.leaveEvent = partial(self.unhighlight, self.books[-1])



    def populate(self):
        """Populates the gallery with books

        Books should be generated by self.generate_books()
        """
        self.clear()
        if self.sort_by.currentText() == 'Alphabetically':
            pass
        elif self.sort_by.currentText() == 'Rating':
            pass
        elif self.sort_by.currentText() == 'Randomly':
            random.shuffle(self.books)

        row_pos = 0
        col_pos = 0
        for book in self.books:
            self.bookshelf.addWidget(book, col_pos, row_pos)

            # calculate next position
            row_pos += 1
            if row_pos > 4: # max 5 columns. aka 5 slots per row
                row_pos = 0
                col_pos += 1

        while col_pos <= 1:
            # if there's only a few books, place invisible frames to shove things into the top left corner
            # this avoids books showing up in the middle and messing up the look of the gallery
            blank = spines.BlankSpine()
            self.bookshelf.addWidget(blank, col_pos, row_pos)

            # calculate next position
            row_pos += 1
            if row_pos > 4: # max 5 columns. aka 5 slots per row
                row_pos = 0
                col_pos += 1



    def clear(self):
        """Clears the gallery of all books
        """
        for i in reversed(range(self.bookshelf.count())):
            self.bookshelf.itemAt(i).widget().setParent(None)



    def select(self, source, event):
        """Selects one or multiple books

        If a book is clicked, it selects just that one book.
        If a book is control + clicked, it selects each book that is clicked this way.
        If a book is shift + clicked, it selects each book between the current click and the last one.

        Args:
            source (QFrame): The frames that represent the book that was double clicked
            event (QMouseEvent): The event that was emitted
        """
        if event.button() != 1: # left click
            return

        if int(event.modifiers()) == 0: # just a normal left click
            self.reset_selected()
            self.selected.append(source)
            self.highlight(source)

        elif event.modifiers() == QtCore.Qt.ControlModifier: # control + click
            # individually select multiple books
            if source in self.selected:
                self.selected.remove(source)
                self.unhighlight(source)
            else:
                self.selected.append(source)
                self.highlight(source)

        elif event.modifiers() == QtCore.Qt.ShiftModifier: # shift + click
            # select all books between the last selection and this new one
            if not self.selected: # don't do anything if there hasn't already been a first selection
                return

            last = self.bookshelf.indexOf(self.selected[-1])
            new = self.bookshelf.indexOf(source)

            if last < new:
                select_queue = self.books[last:new+1]
            else:
                select_queue = self.books[new:last]

            for book in select_queue:
                self.selected.append(book) if book not in self.selected else None
                self.highlight(book)



    def open_book(self, source, event):
        """Opens the reader window to read the book

        Called when a book in the gallery is double clicked

        Args:
            source (QFrame): The frames that represent the book that was double clicked
            event (QMouseEvent): The event that was emitted. Unused, but required by PyQt5
        """
        self.open_book_signal.emit(f'{self.directory}/{source.title}')



    def highlight(self, source, event=None):
        """Highlights a book in the gallery when the mouse hovers over it

        Args:
            source (QFrame): The frames that represent the book that was double clicked
            event (QMouseEvent, optional): The event that was emitted. Unused, but required by PyQt5
        """
        source.setPalette(const.highlight_color)



    def unhighlight(self, source, event=None):
        """Unhighlights a book in the gallery when the mouse leaves the area

        Args:
            source (QFrame): The frames that represent the book that was double clicked
            event (QMouseEvent, optional): The event that was emitted. Unused, but required by PyQt5
        """
        if source not in self.selected:
            source.setPalette(const.default_color)



    def reset_selected(self, event=None):
        """Unhighlights all books and resets self.selected

        Args:
            event (QMouseEvent, optional): The event that was emitted
        """
        if event and event.button() != 1: # left click
            # don't unhighlight if right clicking
            return

        while self.selected:
            self.unhighlight(self.selected.pop())



    def context_menu(self, event):
        """Opens a context menu for the books.

        "Edit": edits the metadata of all currently selected books
        "Open Containing Folder": opens windows explorer for the most recently selected book

        Args:
            event (QMouseEvent): The event that was emitted. Unused, but required by PyQt5
        """
        menu = QMenu()
        edit = menu.addAction('Edit')
        open_ = menu.addAction('Open Containing Folder')
        if (selection := menu.exec_(event.globalPos())):
            # execute
            print(selection.text())