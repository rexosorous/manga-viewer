# standard libraries
from datetime import datetime

# dependencies
from PyQt5.QtWidgets import QFrame

# local modules
from ui.details_frame import Ui_details_panel



class DetailsPanel(QFrame, Ui_details_panel):
    """Allows for editing information about a book.

    Args:
        db (database.DBHandler)
        signals (signals.Signals)

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
        self.populate_series()
        self.connect_events()



    def populate_series(self):
        return

        self.series_dropdown.clear()
        self.series_dropdown.addItem('')
        for series in self.db.get_metadata()['series']:
            self.series_dropdown.addItem(series['name'])



    def connect_events(self):
        self.signals.update_metadata.connect(self.populate_series)



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



    def populate(self, cover_img, book_id):
        return

        self.clear_fields()
        data = self.db.get_book_info(book_id)

        self.cover_img.setPixmap(cover_img)
        self.title_text.setText(data['name'])
        # self.artists_yes_list.
        # self.artists_no_list.
        self.series_dropdown.setCurrentText(data['series'])
        self.order_number.setValue((0 if not data['series_order'] else data['series_order']))
        self.rating_number.setValue((0 if not data['rating'] else data['rating']))
        self.pages_text.setText(str(data['pages']))
        self.date_text.setText(str(datetime.fromtimestamp(data['date_added'])))
        # self.genres_yes_list.
        # self.genres_no_list.
        # self.tags_yes_list.
        # self.tags_no_list.
        self.notes_text.setText(data['notes'])

        for list_item in self.metadata.mdata:
            if list_item.table == 'artists':
                if list_item.id_ in data['artists']:
                    self.artists_yes_list.addItem(list_item)
                else:
                    self.artists_no_list.addItem(list_item)
            elif list_item.table == 'genres':
                if list_item.id_ in data['genres']:
                    self.genres_yes_list.addItem(list_item)
                else:
                    self.genres_no_list.addItem(list_item)
            elif list_item.table == 'tags':
                if list_item.id_ in data['tags']:
                    self.tags_yes_list.addItem(list_item)
                else:
                    self.tags_no_list.addItem(list_item)