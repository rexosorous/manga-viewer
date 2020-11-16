# standard libraries
from datetime import datetime
from functools import partial

# dependencies
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QMessageBox

# local modules
import constants as const
from ui.details_frame import Ui_details_panel



class DetailsPanel(QFrame, Ui_details_panel):
    """Allows for editing information about a book.

    Args:
        db (database.DBHandler)
        signals (signals.Signals)
        book_id (int): ID of the book that this panel is displaying info about. -1 is none selected

    Attributes:
        cover_img (QLabel)
        title_text (QLineEdit)
        artist_text (QLineEdit)
        artist_list (QListWidget)
        series_dropdown (QComboBox)
        order_number (QSpinBox)
        rating_number (QSpinBox)
        pages_text (QLineEdit)
        date_text (QDateEdit)
        genre_text (QLineEdit)
        genre_list (QListWidget)
        tag_text (QLineEdit)
        tag_list (QListWidget)
        notes_text (QTextEdit)
        submit_button (QPushButton)
    """
    def __init__(self, db, signals):
        super().__init__()
        self.setupUi(self)
        self.db = db
        self.signals = signals
        self.book_id = -1
        self.populate_metadata()
        self.connect_events()



    def populate_metadata(self):
        self.clear_fields()

        metadata = self.db.get_metadata()

        # populate series options
        self.series_dropdown.addItem('')
        for series in metadata['series']:
            self.series_dropdown.addItem(series.text(), series.id_)

        # populate metadata lists
        for artist in metadata['artists']:
            self.artists_list.addItem(artist)
        for genre in metadata['genres']:
            self.genres_list.addItem(genre)
        for tag in metadata['tags']:
            self.tags_list.addItem(tag)



    def connect_events(self):
        # typing in the search bars
        self.artists_text.textChanged.connect(partial(self.search_list, self.artists_list))
        self.genres_text.textChanged.connect(partial(self.search_list, self.genres_list))
        self.tags_text.textChanged.connect(partial(self.search_list, self.tags_list))

        # hitting enter in the search bars
        self.artists_text.returnPressed.connect(partial(self.apply_metadata_text, self.artists_text, self.artists_list))
        self.genres_text.returnPressed.connect(partial(self.apply_metadata_text, self.genres_text, self.genres_list))
        self.tags_text.returnPressed.connect(partial(self.apply_metadata_text, self.tags_text, self.tags_list))

        # double clicking a list item
        self.artists_list.itemDoubleClicked.connect(partial(self.apply_metadata, self.artists_list))
        self.genres_list.itemDoubleClicked.connect(partial(self.apply_metadata, self.genres_list))
        self.tags_list.itemDoubleClicked.connect(partial(self.apply_metadata, self.tags_list))

        # buttons
        self.submit_button.clicked.connect(self.submit)

        # signals
        self.signals.populate_details.connect(self.populate_book_info)
        self.signals.depopulate_details.connect(self.cleanse_details)
        self.signals.update_metadata.connect(self.update_metadata)



    def clear_fields(self):
        self.cover_img.clear()
        self.title_text.clear()
        self.artists_text.clear()
        self.artists_list.clear()
        self.series_dropdown.clear()
        self.order_number.setValue(0)
        self.rating_number.setValue(0)
        self.pages_text.clear()
        self.date_text.clear()
        self.genres_text.clear()
        self.genres_list.clear()
        self.tags_text.clear()
        self.tags_list.clear()
        self.notes_text.clear()



    def update_metadata(self):
        """Updates all the metadata when metadata is edited in any way

        Makes sure to re-populate book info if a book is currently selected
        """
        cover_img = self.cover_img.pixmap()
        self.populate_metadata()
        if self.book_id >= 0:
            self.populate_book_info(cover_img, self.book_id)



    def populate_book_info(self, cover_img, book_id):
        self.book_id = book_id
        book_info = self.db.get_book_info(book_id)

        self.cover_img.setPixmap(cover_img)
        self.title_text.setText(book_info['name'])
        self.series_dropdown.setCurrentText(book_info['series'].text())
        self.order_number.setValue((0 if not book_info['series_order'] else book_info['series_order']))
        self.rating_number.setValue((0 if not book_info['rating'] else book_info['rating']))
        self.pages_text.setText(str(book_info['pages']))
        self.date_text.setText(datetime.fromtimestamp(book_info['date_added']).strftime('%B %d, %Y - %I:%M%p'))
        self.notes_text.setText(book_info['notes'])

        for i in range(self.artists_list.count()):
            item = self.artists_list.item(i)
            if item in book_info['artists']:
                self.apply_metadata(self.artists_list, item)

        for i in range(self.genres_list.count()):
            item = self.genres_list.item(i)
            if item in book_info['genres']:
                self.apply_metadata(self.genres_list, item)

        for i in range(self.tags_list.count()):
            item = self.tags_list.item(i)
            if item in book_info['tags']:
                self.apply_metadata(self.tags_list, item)



    def cleanse_details(self):
        """Cleanses info about the currently selected book

        Executed when a book is deselected in the gallery
        """
        self.book_id = -1
        self.populate_metadata()



    def apply_metadata(self, list_widget, item):
        """Applies or unapplies the selected metadata and sorts the list.

        Changes the applied status to the opposite of what it currently is

        Args:
            list_widget (QListWidget)
            item (ListItem)
        """
        # flip flop the applied status
        if item.background() == const.Colors.AND:
            item.setBackground(const.Colors.NONE)
        elif item.background() == const.Colors.NONE:
            item.setBackground(const.Colors.AND)

        # take out all the items in the list and sort them based on their applied status
        applied = []
        unapplied = []
        while len(list_widget): # remove each item and sort them into their appropriate groups
            item = list_widget.takeItem(0)
            if item.background() == const.Colors.AND:
                applied.append(item)
            elif item.background() == const.Colors.NONE:
                unapplied.append(item)

        # sort backwards (explained below)
        applied.sort(key=lambda x: x.text(), reverse=True)
        unapplied.sort(key=lambda x: x.text(), reverse=True)

        # re-add the items in the correct order
        for item in unapplied: # we add everything in backwards because it's easier to insert each item at pos 0 rather than find out what the last pos is
            list_widget.insertItem(0, item)
        for item in applied:
            list_widget.insertItem(0, item)



    def search_list(self, list_widget, search_term):
        """Hides and reveals items in the list widget based on the text being typed in the corresponding line edit

        Args:
            list_widget (QListWidget)
            search_term (str)
        """
        search_term = search_term.lower()
        for i in range(list_widget.count()):
            item = list_widget.item(i)
            if search_term in item.text().lower():
                item.setHidden(False)
            else:
                item.setHidden(True)



    def apply_metadata_text(self, text_widget, list_widget):
        """Applies the filter to the topmost ListItem and then floats it to the top of the list

        Alternatively, the user can use prefixes to determine the filter type.
        Executed when a user hits enter in a listwidget's lineedit.

        Args:
            text_widget (QLineEdit)
            list_widget (QListWidget)
        """
        for i in range(list_widget.count()):
            item = list_widget.item(i)
            if not item.isHidden():
                self.apply_metadata(list_widget, item)
                break

        text_widget.clear()



    def submit(self):
        """Updates a book with new information.
        """
        # make sure a book is selected
        if self.book_id < 0:
            return

        # confirm with user that they actually want to edit the book
        popup = QMessageBox()
        popup.setIcon(QMessageBox.Warning)
        popup.setWindowTitle('Confirm')
        popup.setText(f'Are you sure you want to update this manga\'s metadata?')
        popup.setStandardButtons(QMessageBox.Yes | (no := QMessageBox.Cancel))
        response = popup.exec_()

        if response == no:
            return

        # collect data
        data = dict()
        data['id'] = self.book_id
        data['title'] = self.title_text.text()
        data['series'] = self.series_dropdown.currentData()
        data['series_order'] = (self.order_number.value() if self.order_number.value() else None)
        data['rating'] = (self.rating_number.value() if self.rating_number.value() else None)
        data['notes'] = (self.notes_text.toPlainText() if self.notes_text.toPlainText() else None)

        data['artists'] = []
        for i in range(self.artists_list.count()):
            item = self.artists_list.item(i)
            if item.background() == const.Colors.AND:
                data['artists'].append(item.id_)

        data['genres'] = []
        for i in range(self.genres_list.count()):
            item = self.genres_list.item(i)
            if item.background() == const.Colors.AND:
                data['genres'].append(item.id_)

        data['tags'] = []
        for i in range(self.tags_list.count()):
            item = self.tags_list.item(i)
            if item.background() == const.Colors.AND:
                data['tags'].append(item.id_)

        # make sure title (required field) is filled
        if not data['title']:
            popup = QMessageBox()
            popup.setIcon(QMessageBox.Critical)
            popup.setWindowTitle('Error')
            popup.setText('Missing title!')
            popup.setStandardButtons(QMessageBox.Close)
            popup.exec_()
            return

        # update info
        self.db.update_book(data)
        self.signals.update_spines.emit()

        # inform user of successful operation
        popup = QMessageBox()
        popup.setIcon(QMessageBox.Information)
        popup.setWindowTitle('Success')
        popup.setText(f'{data["title"]} updated successfully')
        popup.setStandardButtons(QMessageBox.Close)
        popup.exec_()