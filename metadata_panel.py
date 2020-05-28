from PyQt5.QtWidgets import QFrame

from ui.metadata_frame import Ui_metadata_panel


class MetadataPanel(QFrame, Ui_metadata_panel):
    def __init__(self):
        super().__init__()
        self.setupUi(self)