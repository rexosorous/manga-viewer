# standard libraries
from functools import partial
from os import listdir
from os.path import relpath
from shutil import rmtree
import random

# dependencies
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QMessageBox

# local modules
import constants as const
from ui.bookshelf_frame import Ui_bookshelf_panel
import reader
import spines



class BookshelfPanel(QFrame, Ui_bookshelf_panel):
    def __init__(self, db, signals):
        super().__init__()
        self.db = db
        self.signals = signals
        self.books = []
        self.selected = None
        self.setupUi(self)
        self.connect_events()
        self.generate_books()



    def connect_events(self):
        """Connects each signal to their respective functions
        """
        # dropdowns
        self.sort_by.currentIndexChanged.connect(self.sort)

        # basic search
        self.search_bar.textChanged.connect(self.basic_search)

        # buttons
        self.random_button.clicked.connect(self.random_select)

        # bookshelf
        self.bookshelf_scroll_area.contextMenuEvent = self.context_menu
        self.bookshelf_scroll_area.mousePressEvent = self.reset_selected

        # signals
        self.signals.update_spine.connect(self.update_spine)
        self.signals.search_advanced.connect(self.generate_books)
        self.signals.delete_book_db.connect(self.delete_book_db) # from spines context menu
        self.signals.delete_book_disk.connect(self.delete_book_disk) # from spines context menu
        self.signals.select_book.connect(self.select)



    def generate_books(self, filters=None):
        """Creates objects for the books based on certain search parameters and then populates the gallery

        Args:
            filters (dict, optional): filters to filter by from search panel
        """
        self.books = []
        books_on_disk = listdir(const.directory)
        books_not_found = []
        for book in self.db.get_books(filters, self.sort_by.currentIndex()):
            if book['directory'] not in books_on_disk: # avoid errors where it can't find the book on disk
                books_not_found.append(book)
                continue

            # set up frame
            spine = spines.BookSpine(self.signals, *book.values())

            # add the new frames to the list
            self.books.append(spine)

            # connect events
            spine.mousePressEvent = partial(self.select, self.books[-1])
            spine.mouseDoubleClickEvent = partial(self.open_book, self.books[-1])
            spine.enterEvent = partial(self.highlight, self.books[-1])
            spine.leaveEvent = partial(self.unhighlight, self.books[-1])

        if books_not_found:
            popup = QMessageBox()
            popup.setIcon(QMessageBox.Critical)
            popup.setWindowTitle('Error')
            popup.setText('Unable to find the following books:\n')
            popup.setInformativeText('\n'.join([book['name'] for book in books_not_found]))
            popup.setStandardButtons(QMessageBox.Close)
            popup.exec_()

        self.populate()



    def populate(self):
        """Populates the gallery with books that MUST FIRST be generated with self.generate_books()
        """
        self.clear()

        col_pos = 0
        row_pos = 0
        for book in self.books:
            if book.hide_:
                continue
            book.row = row_pos
            self.bookshelf_layout.addWidget(book, row_pos, col_pos)

            # calculate next position
            col_pos += 1
            if col_pos > 4: # max 5 columns. aka 5 slots per row
                col_pos = 0
                row_pos += 1

        while row_pos <= 1:
            # if there's only a few books, place invisible frames to shove things into the top left corner
            # this avoids books showing up in the middle and messing up the look of the gallery
            blank = spines.BlankSpine()
            self.bookshelf_layout.addWidget(blank, row_pos, col_pos)

            # calculate next position
            col_pos += 1
            if col_pos > 4: # max 5 columns. aka 5 slots per row
                col_pos = 0
                row_pos += 1

        if (new_select := next((x for x in self.books if x == self.selected), None)):
            self.select(new_select)
        else:
            self.reset_selected()



    def basic_search(self, search_term: str):
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
        self.populate()



    def sort(self, sort: int):
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
        self.populate()



    def clear(self):
        """Clears the gallery of all books
        """
        for i in reversed(range(self.bookshelf_layout.count())):
            self.bookshelf_layout.itemAt(i).widget().clear_mem() # fixes memory leak
            self.bookshelf_layout.itemAt(i).widget().setParent(None)



    def update_spine(self, book_id):
        """Updates a spine that was changed in the details panel
        """
        for book in self.books:
            if book.id_ == book_id:
                book.set_db_data(*self.db.get_book(book_id).values())
                break



    def resizeEvent(self, event):
        if event.size().width() < 1100: # i don't know why but this is called on startup with a small size
            return
        self.resize_spines(event.size().width())



    def resize_spines(self, window_width: int):
        """Resizes all the spines in the gallery when the window is resized.
        Mainly because I can't figure out how to get it to do this automatically with highdpiscaling
        """
        for i in reversed(range(self.bookshelf_layout.count())):
            spine = self.bookshelf_layout.itemAt(i).widget()
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
        reader_window = reader.Reader(self.signals, self.db)
        reader_window.open_book(source.id_)
        reader_window.show()



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



    def random_select(self):
        """Randomly selects a book from the list
        """
        self.select(random.choice(self.books))
        row_height = self.books[0].height() + self.bookshelf_layout.verticalSpacing()
        self.bookshelf_scroll_area.verticalScrollBar().setValue(self.selected.row * row_height)



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
            self.populate()



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
            self.populate()



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
                self.signals.clear_filter.emit()
            if selection == clear_selected:
                self.reset_selected()