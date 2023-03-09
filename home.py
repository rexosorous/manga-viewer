# standard libraries
from datetime import datetime
from functools import partial
from os import listdir
from os.path import isdir
from os.path import relpath
from shutil import rmtree
import random

# dependencies
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QMessageBox

# local modules
import constants as const
import database
from details_panel import DetailsPanel
from metadata_panel import MetadataPanel
from search_panel import SearchPanel
import spines
from ui.main_window import Ui_MainWindow



class Home(QMainWindow, Ui_MainWindow):
    """The main screen

    Args:
        signals (signals.Signals)
        directory (str)

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

        books ([QFrame]): holds a list of all book frames
        selected (QFrame): holds the currently selected book
        details_panel (DetailsPanel)
        search_panel (SearchPanel)
        metadata_panel (MetadataPanel)
    """
    def __init__(self, signals, directory: str):
        super().__init__()
        self.setupUi(self)

        # init attributes
        self.signals = signals
        self.directory = directory
        self.db = database.DBHandler()
        self.books = []
        self.selected = None

        self.details_panel = DetailsPanel(self.db, self.signals)
        self.search_panel = SearchPanel(self.db, self.signals)
        self.metadata_panel = MetadataPanel(self.db, self.signals)
        self.setup_panels()

        self.connect_events()
        self.generate_books()



    def setup_panels(self):
        """Adds all panels to the main layout and makes only the details panel visible
        """
        self.main_area.addWidget(self.details_panel)
        self.main_area.addWidget(self.search_panel)
        self.main_area.addWidget(self.metadata_panel)
        self.search_panel.setVisible(False)
        self.metadata_panel.setVisible(False)



    def connect_events(self):
        """Connects each signal to their respective functions
        """
        # toolbar
        self.scan_button.triggered.connect(self.scan_directory)
        # self.change_directory_button.triggered.connect()
        # self.backup_database_button.triggered.connect()
        # self.load_database_button.triggered.conenct()

        # dropdowns
        self.sort_by.currentIndexChanged.connect(self.sort_gallery)

        # basic search
        self.search_bar.textChanged.connect(self.search_gallery)

        # buttons
        self.details_button.clicked.connect(lambda : [self.details_panel.setVisible(True), self.search_panel.setVisible(False), self.metadata_panel.setVisible(False)])
        self.advanced_search_button.clicked.connect(lambda : [self.details_panel.setVisible(False), self.search_panel.setVisible(True), self.metadata_panel.setVisible(False)])
        self.metadata_button.clicked.connect(lambda : [self.details_panel.setVisible(False), self.search_panel.setVisible(False), self.metadata_panel.setVisible(True)])
        self.random_button.clicked.connect(self.random_select)

        # bookshelf
        self.bookshelf_area.contextMenuEvent = self.context_menu
        self.bookshelf_area.mousePressEvent = self.reset_selected

        # signals
        self.signals.update_spine.connect(self.update_spine)
        self.signals.search_advanced.connect(self.generate_books)
        self.signals.delete_book_db.connect(self.delete_book_db) # from spines context menu
        self.signals.delete_book_disk.connect(self.delete_book_disk) # from spines context menu



    def scan_directory(self):
        """Scans the manga directory for any new entries, adds the new books to the db with near blank fields, and then sets the search filter to only show the new books so the user can edit the metadata
        """
        scan_time = datetime.now()
        for book in (folder for folder in listdir(const.directory) if isdir(f'{const.directory}/{folder}') and folder not in self.db.get_book_directories()):
            self.db.add_book(book, book, pages=len(listdir(f'{const.directory}/{book}')))

        # filter gallery to show only the the new books (using date filtering)
        # show search_panel with the filter we set
        self.details_panel.setVisible(False)
        self.search_panel.setVisible(True)
        self.metadata_panel.setVisible(False)
        self.search_panel.clear_fields()
        self.search_panel.date_low.setDateTime(scan_time)
        self.search_panel.submit()



    def random_select(self):
        """Randomly selects a book from the list
        """
        self.select(random.choice(self.books))



    def generate_books(self, filters=None):
        """Creates objects for the books based on certain search parameters and then populates the gallery

        Args:
            filters (dict, optional): filters to filter by from search panel
        """
        self.books = []
        for book in self.db.get_books(filters, self.sort_by.currentIndex()):
            # set up frame
            spine = spines.BookSpine(self.signals, *book.values())

            # add the new frames to the list
            self.books.append(spine)

            # connect events
            spine.mousePressEvent = partial(self.select, self.books[-1])
            spine.mouseDoubleClickEvent = partial(self.open_book, self.books[-1])
            spine.enterEvent = partial(self.highlight, self.books[-1])
            spine.leaveEvent = partial(self.unhighlight, self.books[-1])
        self.populate_gallery()



    def populate_gallery(self):
        """Populates the gallery with books that MUST FIRST be generated with self.generate_books()
        """
        self.clear_gallery()

        row_pos = 0
        col_pos = 0
        for book in self.books:
            if book.hide_:
                continue
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

        if (new_select := next((x for x in self.books if x == self.selected), None)):
            self.select(new_select)
        else:
            self.reset_selected()



    def search_gallery(self, search_term: str):
        '''Basic search

        Only searches titles and alt_titles of what's in the gallery. So if there's already a filter applied, it won't show books beyond the filter.
        '''
        for book in self.books:
            if search_term.lower() in book.title.lower():
                book.hide_ = False
            elif book.alt_title and search_term.lower() in book.alt_title.lower():
                book.hide_ = False
            else:
                book.hide_ = True
        self.populate_gallery()



    def sort_gallery(self, sort: int):
        """Re-sorts the books in the gallery when self.sort_by is changed
        """
        if not self.books: # sorting books when there are no books causes a crash
            return
        if sort == const.Sort.ALPHA_ASC:
            self.books = sorted(self.books, key=lambda spine: spine.title)
        elif sort == const.Sort.ALPHA_DESC:
            self.books = sorted(self.books, key=lambda spine: spine.title, reverse=True)
        elif sort == const.Sort.RATING_ASC:
            self.books = sorted(self.books, key=lambda spine: spine.rating or -1)
        elif sort == const.Sort.RATING_DESC:
            self.books = sorted(self.books, key=lambda spine: spine.rating or -1, reverse=True)
        elif sort == const.Sort.PAGES_ASC:
            self.books = sorted(self.books, key=lambda spine: spine.pages)
        elif sort == const.Sort.PAGES_DESC:
            self.books = sorted(self.books, key=lambda spine: spine.pages, reverse=True)
        elif sort == const.Sort.DATE_ASC:
            self.books = sorted(self.books, key=lambda spine: spine.date_added)
        elif sort == const.Sort.DATE_DESC:
            self.books = sorted(self.books, key=lambda spine: spine.date_added, reverse=True)
        elif sort == const.Sort.RANDOM:
            random.shuffle(self.books)
        self.populate_gallery()



    def clear_gallery(self):
        """Clears the gallery of all books
        """
        for i in reversed(range(self.bookshelf.count())):
            self.bookshelf.itemAt(i).widget().setParent(None)



    def update_spine(self, book_id):
        """Updates a spine that was changed in the details panel
        """
        for book in self.books:
            if book.id_ == book_id:
                book.set_db_data(*self.db.get_book(book_id).values())
                break



    def resizeEvent(self, event):
        self.resize_gallery(event.size().width())



    def resize_gallery(self, window_width: int):
        """Resizes all the spines in the gallery when the window is resized.
        Mainly because I can't figure out how to get it to do this automatically with highdpiscaling
        """
        for i in reversed(range(self.bookshelf.count())):
            spine = self.bookshelf.itemAt(i).widget()
            spine.resize(window_width)



    def select(self, source, event=None):
        """Selects one of the books only.

        Args:
            source (QFrame): The frames that represent the book that was double clicked
            event (QMouseEvent, optional): The event that was emitted
        """
        if not event or event.button() == 1: # left click
            self.reset_selected()
            self.selected = source
            self.highlight(source)
            self.signals.populate_details.emit(source.loaded_image, source.id_)



    def open_book(self, source, event):
        """Opens the reader window to read the book

        Called when a book in the gallery is double clicked

        Args:
            source (QFrame): The frames that represent the book that was double clicked
            event (QMouseEvent): The event that was emitted. Unused, but required by PyQt5
        """
        self.signals.open_book_signal.emit(source.id_, source.title, f'{self.directory}/{source.folder}')



    def highlight(self, source, event=None):
        """Highlights a book in the gallery when the mouse hovers over it

        Args:
            source (QFrame): The frames that represent the book that was double clicked
            event (QMouseEvent, optional): The event that was emitted. Unused, but required by PyQt5
        """
        source.setPalette(const.Palettes.HIGHLIGHT)



    def unhighlight(self, source, event=None, absolute=False):
        """Unhighlights a book in the gallery when the mouse leaves the area

        Args:
            source (QFrame): The frames that represent the book that was double clicked
            absolute (bool): if true, will unhighlight regardless of if that book is selected
            event (QMouseEvent, optional): The event that was emitted. Unused, but required by PyQt5
        """
        if source and (source != self.selected or absolute):
            source.setPalette(const.Palettes.PRIMARY)



    def reset_selected(self, event=None):
        """Unhighlights all books and resets self.selected

        Args:
            event (QMouseEvent, optional): The event that was emitted
        """
        if not event or event.button() == 1: # left click
            self.unhighlight(self.selected, None, True)
            self.selected = None
            self.signals.depopulate_details.emit()



    def delete_book_db(self, book: spines.BookSpine):
        popup = QMessageBox()
        popup.setIcon(QMessageBox.Warning)
        popup.setWindowTitle('Confirm')
        popup.setText(f'Are you sure you want to delete {book.title} from the database?')
        popup.setInformativeText('Note: this will not delete the files from disk.')
        popup.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        selection = popup.exec_()
        if selection == QMessageBox.Ok:
            self.db.delete_book(book.id_)
            self.reset_selected()
            self.books.remove(book)
            self.populate_gallery()



    def delete_book_disk(self, book: spines.BookSpine):
        popup = QMessageBox()
        popup.setIcon(QMessageBox.Warning)
        popup.setWindowTitle('Confirm')
        popup.setText(f'Are you sure you want to delete {book.title} from both the DB and disk?')
        popup.setInformativeText('Note: THIS CANNOT BE UNDONE. FILES CANNOT BE RECOVERED')
        popup.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        selection = popup.exec_()
        if selection == QMessageBox.Ok:
            self.db.delete_book(book.id_)
            self.reset_selected()
            self.books.remove(book)
            rmtree(relpath(f'{const.directory}/{book.folder}'))
            self.populate_gallery()



    def context_menu(self, event):
        """Opens a context menu for the books.

        "Clear Filter": removes all filters from the search_panel to show all books
        "Clear Selected": deselects the currently selected book

        Args:
            event (QMouseEvent): The event that was emitted. Unused, but required by PyQt5
        """
        menu = QMenu()
        clear_filter = menu.addAction('Clear Filter')
        clear_selected = menu.addAction('Clear Selected')
        if (selection := menu.exec_(event.globalPos())):
            if selection == clear_filter:
                self.details_panel.setVisible(False)
                self.search_panel.setVisible(True)
                self.metadata_panel.setVisible(False)
                self.search_panel.clear_fields()
                self.search_panel.submit()
            if selection == clear_selected:
                self.reset_selected()