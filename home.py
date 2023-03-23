# standard libraries
from datetime import datetime
from datetime import timedelta
import json
from os import listdir
from os.path import isdir

# dependencies
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMainWindow

# local modules
import constants as const
import database
from bookshelf_panel import BookshelfPanel
from details_panel import DetailsPanel
from metadata_panel import MetadataPanel
from search_panel import SearchPanel
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

        gallery_layout (QHBoxLayout)
        bookshelf (QGridLayout): the layout where all the books will be displayed
        bookshelf_scroll_area (QScrollArea): the whole area where books will be displayed

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

        self.bookshelf_panel = BookshelfPanel(self.db, self.signals)
        self.details_panel = DetailsPanel(self.db, self.signals)
        self.search_panel = SearchPanel(self.db, self.signals)
        self.metadata_panel = MetadataPanel(self.db, self.signals)
        self.setup_panels()

        self.connect_events()



    def setup_panels(self):
        """Adds all panels to the main layout and makes only the details panel visible
        """
        self.gallery_layout.addWidget(self.bookshelf_panel)
        self.gallery_layout.addWidget(self.details_panel)
        self.gallery_layout.addWidget(self.search_panel)
        self.gallery_layout.addWidget(self.metadata_panel)
        self.details_panel.setVisible(False)
        self.search_panel.setVisible(False)
        self.metadata_panel.setVisible(False)



    def connect_events(self):
        """Connects each signal to their respective functions
        """
        # toolbar
        self.scan_button.triggered.connect(self.scan_directory)
        self.change_directory_button.triggered.connect(self.change_directory)

        # buttons
        self.bookshelf_button.clicked.connect(self.show_bookshelf_panel)
        self.details_button.clicked.connect(self.show_details_panel)
        self.advanced_search_button.clicked.connect(self.show_advanced_search_panel)
        self.metadata_button.clicked.connect(self.show_metadata_panel)

        # signals
        self.signals.show_details_panel.connect(self.show_details_panel)
        self.signals.show_bookshelf_panel.connect(self.show_bookshelf_panel)



    def show_bookshelf_panel(self):
        self.bookshelf_panel.setVisible(True)
        self.details_panel.setVisible(False)
        self.search_panel.setVisible(False)
        self.metadata_panel.setVisible(False)

        self.bookshelf_button.setEnabled(False)
        self.details_button.setEnabled(True)
        self.advanced_search_button.setEnabled(True)
        self.metadata_button.setEnabled(True)



    def show_details_panel(self):
        self.bookshelf_panel.setVisible(False)
        self.details_panel.setVisible(True)
        self.search_panel.setVisible(False)
        self.metadata_panel.setVisible(False)

        self.bookshelf_button.setEnabled(True)
        self.details_button.setEnabled(False)
        self.advanced_search_button.setEnabled(True)
        self.metadata_button.setEnabled(True)



    def show_advanced_search_panel(self):
        self.bookshelf_panel.setVisible(False)
        self.details_panel.setVisible(False)
        self.search_panel.setVisible(True)
        self.metadata_panel.setVisible(False)

        self.bookshelf_button.setEnabled(True)
        self.details_button.setEnabled(True)
        self.advanced_search_button.setEnabled(False)
        self.metadata_button.setEnabled(True)



    def show_metadata_panel(self):
        self.bookshelf_panel.setVisible(False)
        self.details_panel.setVisible(False)
        self.search_panel.setVisible(False)
        self.metadata_panel.setVisible(True)

        self.bookshelf_button.setEnabled(True)
        self.details_button.setEnabled(True)
        self.advanced_search_button.setEnabled(True)
        self.metadata_button.setEnabled(False)



    def scan_directory(self):
        """Scans the manga directory for any new entries, adds the new books to the db with near blank fields, and then sets the search filter to only show the new books so the user can edit the metadata
        """
        scan_time = datetime.now()
        for book in (folder for folder in listdir(const.directory) if isdir(f'{const.directory}/{folder}') and folder not in self.db.get_book_directories()):
            self.db.add_book(book, book, pages=len(listdir(f'{const.directory}/{book}')))

        # filter gallery to show only the the new books (using date filtering)
        self.show_details_panel()
        self.search_panel.clear_fields()
        self.search_panel.date_low.setDateTime(scan_time - timedelta(minutes=1))
        self.search_panel.submit()



    def change_directory(self):
        choose_folder = QFileDialog()
        choose_folder.setFileMode(QFileDialog.FileMode.DirectoryOnly)
        if choose_folder.exec_():
            folder = choose_folder.selectedFiles()

        with open('config.json', 'r') as file:
            data = json.load(file)
        data['directory'] = folder[0]
        with open('config.json', 'w') as file:
            json.dump(data, file)
        const.directory = folder[0]

        self.search_panel.submit()