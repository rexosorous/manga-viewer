# dependencies
from PyQt5.QtWidgets import QFrame

# local modules
from ui.details_frame import Ui_details_panel



class DetailsPanel(QFrame, Ui_details_panel):
    def __init__(self):
        super().__init__()
        self.setupUi(self)