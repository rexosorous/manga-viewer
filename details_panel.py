# dependencies
from PyQt5.QtWidgets import QFrame

# local modules
from ui.details_frame import Ui_details_panel



class DetailsPanel(QFrame, Ui_details_panel):
    """Allows for editing information about a book.

    Args:
        metadata (metadata.Data)
        signals (signals.Signals)

    Attributes:
        cover_img (QLabel)
        title_text (QLineEdit)
        artists_text (QLineEdit)
        artists_dropdown (QComboBox)
        artists_list (QListWidget)
        series_text (QLineEdit)
        series_dropdown (QComboBox)
        order_number (QSpinBox)
        rating_number (QSpinBox)
        pages_text (QLineEdit)
        date_text (QLineEdit)
        genres_text(QLineEdit)
        genres_dropdown (QComboBox)
        genres_list (QListWidget)
        tags_text (QLineEdit)
        tags_dropdown (QComboBox)
        tags_list (QListWidget)
        notes_text (QTextEdit)
        submit_button (QPushButton)
    """
    def __init__(self, metadata, signals):
        super().__init__()
        self.setupUi(self)
        self.metadata = metadata
        self.signals = signals
        self.connect_events()



    def connect_events(self):
        # self.signals.update_metadata.connect()
        pass



    def clear_fields(self):
        pass



    def populate(self, book_id):
        self.clear_fields()