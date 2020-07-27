# dependencies
from PyQt5.QtWidgets import QFrame

# local modules
from ui.search_frame import Ui_search_panel



class SearchPanel(QFrame, Ui_search_panel):
    def __init__(self):
        super().__init__()
        self.setupUi(self)