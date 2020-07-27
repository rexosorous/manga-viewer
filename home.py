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
from details_panel import DetailsPanel
from search_panel import SearchPanel
from metadata_panel import MetadataPanel
import database
import metadata
import signals



"""
TODO
    * implement search bar functionality
    * implement sorting
    * write logic for side panels (editing book details and search filter)
    * figure out how to handle batch editing
"""

class Home(QMainWindow, Ui_MainWindow):
    """Window used to read pages in the manga

    Attributes:
        search_bar (QLineEdit)
        search_button (QPushButton): same function as pressing entet in search bar
        details_button (QPushButton)
        advanced_search_button (QPushButton): opens a new window with all searchable options
        metadata_button (QPushButton):
        sort_by (QComboBox): contains "Alphabetically", "Rating", and "Randomly"
        random_button (QPushButton): randomly selects from the list

        main_area (QHBoxLayout)
        bookshelf (QGridLayout): the layout where all the books will be displayed
        bookshelf_area (QScrollArea): the whole area where books will be displayed

        open_book_signal (pyqtSignal): triggered to open a book to read
        books ([QFrame]): holds a list of all book frames
        selected ([QFrame]): holds all currently selected books
        details_panel (DetailsPanel)
        search_panel (SearchPanel)
        metadata_panel (MetadataPanel)
    """
    open_book_signal = QtCore.pyqtSignal(str)

    def __init__(self, directory):
        super().__init__()
        self.setupUi(self)

        # init attributes
        self.db = database.DBHandler()
        self.directory = directory
        self.books = []
        self.selected = []
        self.signals = signals.Signals()

        self.metadata = metadata.Data(self.db, self.signals)
        self.details_panel = DetailsPanel()
        self.search_panel = SearchPanel()
        self.metadata_panel = MetadataPanel(self.metadata, self.signals)
        self.setup_panels()

        self.connect_signals()
        self.generate_books()
        self.populate_gallery()



    def setup_panels(self):
        """Adds all panels to the main layout and makes only the details panel visible
        """
        self.main_area.addWidget(self.details_panel)
        self.main_area.addWidget(self.search_panel)
        self.main_area.addWidget(self.metadata_panel)
        self.search_panel.setVisible(False)
        self.metadata_panel.setVisible(False)



    def connect_signals(self):
        """Connects each signal to their respective functions
        """
        self.details_button.clicked.connect(lambda : [self.details_panel.setVisible(True), self.search_panel.setVisible(False), self.metadata_panel.setVisible(False)])
        self.advanced_search_button.clicked.connect(lambda : [self.details_panel.setVisible(False), self.search_panel.setVisible(True), self.metadata_panel.setVisible(False)])
        self.metadata_button.clicked.connect(lambda : [self.details_panel.setVisible(False), self.search_panel.setVisible(False), self.metadata_panel.setVisible(True)])
        self.sort_by.currentIndexChanged.connect(self.populate_gallery)
        self.random_button.clicked.connect(self.random_select)
        self.bookshelf_area.contextMenuEvent = self.context_menu
        self.bookshelf_area.mousePressEvent = self.reset_selected
        self.bookshelf_area.keyPressEvent = self.keyboard_handler



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
        # for book in listdir(f'{self.directory}/'):
        for book in self.db.get_books():
            # set up frame
            spine = spines.BookSpine(book['id'], book['name'], book['directory'])

            # add the new frames to the list
            self.books.append(spine)

            # connect events
            spine.mousePressEvent = partial(self.select, self.books[-1])
            spine.mouseDoubleClickEvent = partial(self.open_book, self.books[-1])
            spine.enterEvent = partial(self.highlight, self.books[-1])
            spine.leaveEvent = partial(self.unhighlight, self.books[-1])



    def populate_gallery(self):
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
        self.open_book_signal.emit(f'{self.directory}/{source.folder}')



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
            source.setPalette(const.primary_color)



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