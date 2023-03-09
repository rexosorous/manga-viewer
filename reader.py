# standard libraries
from os import listdir

# dependencies
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QShortcut

# local modules
from ui.reader_window import Ui_MainWindow
from ui.page_preview import Ui_page_preview
import constants as const



class PagePreview(Ui_page_preview, QFrame):
    '''
    Done this way because adding images to a qlistwidget is pretty annoying and this allows padding/margins
    for highlighting purposes
    '''
    def __init__(self, text: int, image: QPixmap):
        super().__init__()
        self.setupUi(self)

        pixmap = image.copy() # deep copy so it doesn't effect the original
        pixmap = pixmap.scaledToWidth(100, Qt.SmoothTransformation)
        self.img_label.setPixmap(pixmap)
        self.img_label.setFixedHeight(pixmap.size().height())
        self.text_label.setText(text)
        self.text_label.setFixedHeight(self.text_label.heightForWidth(100))


    def adjust(self):
        '''
        When wrapping text, the label resizes properly, but doesn't tell the frame that it also needs to resize. This fixes the height issues that occur resulting from that
        '''
        height = self.img_label.height() + self.text_label.height() + self.verticalLayout.getContentsMargins()[0] + self.verticalLayout.getContentsMargins()[2] + self.verticalLayout.spacing()
        self.setFixedHeight(height)



class SeriesPreview(PagePreview):
    '''
    Page Preview for Series
    Done this way because the list items needs to have additional properties
    '''
    def __init__(self, book_id: int, book_title: str, order: int, book_directory: str):
        super().__init__(f'{order} - {book_title}', QPixmap(f'{const.directory}/{book_directory}/{listdir(const.directory + "/" + book_directory)[0]}'))
        self.order = order
        self.book_id = book_id
        self.book_title = book_title
        self.book_directory = book_directory



class Reader(QMainWindow, Ui_MainWindow):
    """Window used to read pages in the manga

    Args:
        signals (signals.Signals)

    Attributes:
        signals (signals.Signals)
        image (QLabel): label used to load pixmaps onto
        page_list (QListWidget): shows all pages, allowing the user to select one to jump to
        series_list (QListWidget): shows all books in the series, allowing the user to jump to a sequel or prequel
        pages ([str]): holds filenames for each page in the book
        current_page (int): the page of the book currently being viewed. 0 for the first page
        size (float): size multiplier. ex: 1 means 100%, 1.1 means 110%, 0.9 means 90%
    """
    def __init__(self, signals, db):
        super().__init__()
        self.setupUi(self)

        # init attributes
        self.signals = signals
        self.db = db
        self.book_id = -1
        self.book_title = '' # unused, but useful to keep it here if needed in the future
        self.directory = ''
        self.pages = []
        self.series = []
        self.size = 1

        self.connect_events()



    def connect_events(self):
        # add hotkeys
        QShortcut(Qt.Key_Right, self, self.next_page)
        QShortcut(Qt.Key_Left, self, self.prev_page)
        QShortcut(Qt.Key_Equal, self, self.zoom_in)
        QShortcut(Qt.Key_Minus, self, self.zoom_out)
        QShortcut(Qt.Key_Escape, self, self.close)

        self.page_list.currentRowChanged.connect(self.draw)
        self.series_list.itemDoubleClicked.connect(self.open_book_in_series)
        self.page_list.itemDoubleClicked.connect(self.open_book_in_series)

        # right click context menu
        self.contextMenuEvent = self.context_menu



    def open_book_in_series(self, item):
        book = self.series_list.itemWidget(item)
        self.open_book(book.book_id, book.book_title, f'{const.directory}/{book.book_directory}')



    def open_book(self, book_id: int, book_title: str, book_directory: str):
        """Loads a book's pages

        Args:
            book_directory (str): the relative directory to find the book
        """
        self.book_id = book_id
        self.book_title = book_title
        self.directory = book_directory
        self.pages = self.get_imgs()
        self.draw(0)
        self.populate_page_list()
        self.populate_series_list()
        self.pages_series_tab_widget.setCurrentIndex(0)



    def populate_page_list(self):
        self.page_list.clear()
        for index, page in enumerate(self.pages):
            item = QListWidgetItem()
            self.page_list.addItem(item)

            card = PagePreview(f'Page {index+1}', page)
            self.page_list.setItemWidget(item, card)
            card.adjust()
            item.setSizeHint(card.size())

        self.page_list.setSpacing(10)
        self.page_list.setCurrentRow(0)



    def populate_series_list(self):
        self.series_list.clear()
        for book in self.db.get_series_for(self.book_id):
            item = QListWidgetItem()
            self.series_list.addItem(item)

            card = SeriesPreview(*book.values())
            self.series_list.setItemWidget(item, card)
            card.adjust()
            item.setSizeHint(card.size())

            if book['id'] == self.book_id:
                self.series_list.setCurrentItem(item)

        self.series_list.setSpacing(10)



    def next_page(self):
        """Displays the next page in the book

        Triggered by right arrow key
        """
        load_page = self.page_list.currentRow() + 1
        if load_page >= len(self.pages): # prevent index out of range error
            load_page = len(self.pages) - 1
        self.page_list.setCurrentRow(load_page)



    def prev_page(self):
        """Displays the previous page in the book

        Triggered by left arrow key
        """
        load_page = self.page_list.currentRow() - 1
        if load_page <= 0: # prevent index out of range error
            load_page = 0
        self.page_list.setCurrentRow(load_page)



    def zoom_in(self):
        """Zooms the page in by 5%

        Triggered by =/+
        """
        self.size += 0.05
        self.draw(self.page_list.currentRow())



    def zoom_out(self):
        """Zooms out the page by 5%

        Triggered by -/_
        """
        self.size -= 0.05
        if self.size < 0.05: # don't let users zoom out to below 5% of the original picture size
            self.size = 0.05
        self.draw(self.page_list.currentRow())



    def get_imgs(self) -> list[QPixmap]:
        """Gets a list of all image files in a folder

        Returns:
            [str]: a relative directory for each file
        """
        return [QPixmap(f'{self.directory}/{x}') for x in listdir(f'{self.directory}/')]



    def draw(self, page: int):
        """Displays a page in the book

        Also resizes the image and moves the scrollbar back to the top
        """
        pixmap = self.pages[page].copy() # deep copy so it doesn't effeect the original
        pixmap = pixmap.scaled(int(pixmap.width()*self.size), int(pixmap.height()*self.size), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image.setPixmap(pixmap)
        self.scrollArea.verticalScrollBar().setSliderPosition(0)



    def close(self):
        """Closes this window and switches back to the home window

        Called when the back button is pressed or the escape key is pressed
        """
        self.signals.close_book_signal.emit()



    def context_menu(self, event):
        """Opens a context menu for the reader

        "Close": same as pressing esc - closes this window
        "Reset Zoom": resets zoom level to 1.0 / 100%

        Args:
            event (QMouseEvent): The event that was emitted. Unused, but required by PyQt5
        """
        menu = QMenu()
        close = menu.addAction('Close')
        reset_zoom = menu.addAction('Reset Zoom')
        page_one = menu.addAction('Go Back To Page 1')
        if (selection := menu.exec_(event.globalPos())):
            if selection == close:
                self.close()
            elif selection == reset_zoom:
                self.size = 1
                self.draw(self.page_list.currentRow())
            elif selection == page_one:
                self.page_list.setCurrentRow(0)