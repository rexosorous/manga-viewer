# dependencies
from PyQt5.QtWidgets import QFrame

# local modules
from ui.search_frame import Ui_search_panel



class SearchPanel(QFrame, Ui_search_panel):
    """Advanced Search

    Attributes:
        title_text (QLineEdit)
        artists_text (QLineEdit)
        artists_dropdown (QComboBox)
        artists_list (QListWidget)
        series_text (QLineEdit)
        series_dropdown (QComboBox)
        series_list (QListWidget)
        order_number (QSpinBox)
        rating_number (QSpinBox)
        rating_toggle (QCheckBox)
        genres_text (QLineEdit)
        genres_dropdown (QComboBox)
        genres_list (QListWidget)
        tags_text (QLineEdit)
        tags_dropdown (QComboBox)
        tags_list (QListWidget)
        submit_button (QPushButton)
    """
    def __init__(self):
        super().__init__()
        self.setupUi(self)