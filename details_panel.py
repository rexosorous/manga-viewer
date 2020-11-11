# standard libraries
from datetime import datetime
from functools import partial

# dependencies
from PyQt5.QtCore import QMimeData
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QMessageBox

# local modules
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
        artists_yes_text (QLineEdit)
        artists_yes_list (QListWidget)
        artists_no_text (QLineEdit)
        artists_no_list (QListWidget)
        series_dropdown (QComboBox)
        order_number (QSpinBox)
        rating_number (QSpinBox)
        pages_text (QLineEdit)
        date_text (QDateEdit)
        genres_yes_text (QLineEdit)
        genres_yes_list (QListWidget)
        genres_no_text (QLineEdit)
        genres_no_list (QListWidget)
        tags_yes_text (QLineEdit)
        tags_yes_list (QListWidget)
        tags_no_text (QLineEdit)
        tags_no_list (QListWidget)
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
        selected_series = self.series_dropdown.currentText()

        # clear fields
        self.series_dropdown.clear()
        self.artists_no_list.clear()
        self.genres_no_list.clear()
        self.tags_no_list.clear()

        # populate series options
        self.series_dropdown.addItem('')
        for series in self.db.get_metadata()['series']:
            self.series_dropdown.addItem(series.text(), series.id_)

        # select the correct series
        self.series_dropdown.setCurrentText(selected_series)

        # populate metadata
        metadata = self.db.get_metadata()
        for artist in metadata['artists']:
            self.artists_no_list.addItem(artist)
        for genre in metadata['genres']:
            self.genres_no_list.addItem(genre)
        for tag in metadata['tags']:
            self.tags_no_list.addItem(tag)

        # remove any metadata that is in yes_list
        for pos in reversed(range(self.artists_no_list.count())):
            if self.artists_no_list.item(pos) in self.get_list_items(self.artists_yes_list):
                self.artists_no_list.takeItem(pos)

        for pos in reversed(range(self.genres_no_list.count())):
            if self.genres_no_list.item(pos) in self.get_list_items(self.genres_yes_list):
                self.genres_no_list.takeItem(pos)

        for pos in reversed(range(self.tags_no_list.count())):
            if self.tags_no_list.item(pos) in self.get_list_items(self.tags_yes_list):
                self.tags_no_list.takeItem(pos)



    def connect_events(self):
        self.signals.update_metadata.connect(self.populate_metadata)
        self.artists_yes_list.itemDoubleClicked.connect(partial(self.move_item, self.artists_yes_list))
        self.artists_no_list.itemDoubleClicked.connect(partial(self.move_item, self.artists_no_list))
        self.genres_yes_list.itemDoubleClicked.connect(partial(self.move_item, self.genres_yes_list))
        self.genres_no_list.itemDoubleClicked.connect(partial(self.move_item, self.genres_no_list))
        self.tags_yes_list.itemDoubleClicked.connect(partial(self.move_item, self.tags_yes_list))
        self.tags_no_list.itemDoubleClicked.connect(partial(self.move_item, self.tags_no_list))
        self.submit_button.clicked.connect(self.submit)



    def get_list_items(self, list_widget):
        """Returns a list of ListItem that are present in a list

        Unfortuantely, PyQt5 does not already have a built in function like this.

        Args:
            list_widget (QListWidget)

        Returns:
            [ListItem]
        """
        items = []
        for i in range(list_widget.count()):
            items.append(list_widget.item(i))
        return items



    def clear_fields(self):
        self.cover_img.clear()
        self.title_text.clear()
        self.artists_yes_text.clear()
        self.artists_yes_list.clear()
        self.artists_no_text.clear()
        self.artists_no_list.clear()
        self.series_dropdown.setCurrentIndex(0)
        self.order_number.setValue(0)
        self.rating_number.setValue(0)
        self.pages_text.clear()
        self.date_text.clear()
        self.genres_yes_text.clear()
        self.genres_yes_list.clear()
        self.genres_no_text.clear()
        self.genres_no_list.clear()
        self.tags_yes_text.clear()
        self.tags_yes_list.clear()
        self.tags_no_text.clear()
        self.tags_no_list.clear()
        self.notes_text.clear()

        self.populate_metadata()



    def populate(self, cover_img, book_id):
        self.book_id = book_id
        self.clear_fields()
        book_info = self.db.get_book_info(book_id)

        self.cover_img.setPixmap(cover_img)
        self.title_text.setText(book_info['name'])
        self.series_dropdown.setCurrentText(book_info['series'].text())
        self.order_number.setValue((0 if not book_info['series_order'] else book_info['series_order']))
        self.rating_number.setValue((0 if not book_info['rating'] else book_info['rating']))
        self.pages_text.setText(str(book_info['pages']))
        self.date_text.setText(datetime.fromtimestamp(book_info['date_added']).strftime('%B %d, %Y - %I:%M%p'))
        self.notes_text.setText(book_info['notes'])

        for artist in book_info['artists']:
            self.artists_yes_list.addItem(artist)
        for genre in book_info['genres']:
            self.genres_yes_list.addItem(genre)
        for tag in book_info['tags']:
            self.tags_yes_list.addItem(tag)

        self.populate_metadata()



    def move_item(self, source, item):
        """When an item is double clicked, remove it from that list and place it in the opposite list (yes to no and vice versa)

        Args:
            source (QListWidget)
            item (ListItem)
        """
        list_picker = {
            'artists_yes_list': self.artists_no_list,
            'artists_no_list': self.artists_yes_list,
            'genres_yes_list': self.genres_no_list,
            'genres_no_list': self.genres_yes_list,
            'tags_yes_list': self.tags_no_list,
            'tags_no_list': self.tags_yes_list
        }

        move = source.takeItem(source.row(item))
        list_picker[source.objectName()].addItem(move)



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
        data['artists'] = [x.id_ for x in self.get_list_items(self.artists_yes_list)]
        data['genres'] = [x.id_ for x in self.get_list_items(self.genres_yes_list)]
        data['tags'] = [x.id_ for x in self.get_list_items(self.tags_yes_list)]

        # make sure required field, title, is filled
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