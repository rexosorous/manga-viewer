# dependencies
from PyQt5.QtWidgets import QFrame

# local modules
from ui.details_frame import Ui_details_panel



class DetailsPanel(QFrame, Ui_details_panel):
    """Allows for editing information about a book.

    Args:
        metadata (metadata.Data)
        signals (signals.Signals)
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