# standard libraries
from os import listdir

# dependencies
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QFont
from PyQt5 import QtCore

# local modules
import constants as const



class BookSpine(QtWidgets.QFrame):
    """Custom QFrame object to display in the bookshelf

    Done this way partially to abstract away the frame creation, but mainly to hold instance variables

    Args:
        title (str): the title of the book
        directory (str): the base directory of all the books. NOT the directory of this specific book.

    Attributes:
        title (str)
        layout (QVBoxLayout)
    """
    def __init__(self, title: str, directory: str):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout()
        self.title = title

        self.setup_frame()
        self.setup_layout()
        self.setup_img(directory)
        self.setup_title()

    def setup_frame(self):
        self.setFixedWidth(const.spine_width)
        self.setFixedHeight(const.spine_height)
        self.setFrameShape(QtWidgets.QFrame.Box)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.setContentsMargins(3, 3, 3, 3)
        self.setPalette(const.default_color)
        self.setAutoFillBackground(True)

    def setup_layout(self):
        self.layout.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)
        self.setLayout(self.layout)

    def setup_img(self, directory):
        img = QtWidgets.QLabel()
        img.setFixedWidth(const.spine_img_width)
        img.setFixedHeight(const.spine_img_height)
        img.setAlignment(QtCore.Qt.AlignCenter)
        img.setContentsMargins(0, 0, 0, 0)
        pixmap = QPixmap(f'{directory}/{self.title}/{listdir(f"{directory}/{self.title}/")[0]}')
        pixmap = pixmap.scaledToHeight(const.spine_img_height, QtCore.Qt.SmoothTransformation)
        crop = QtCore.QRect((pixmap.width() - const.spine_img_width) / 2, (pixmap.height() - const.spine_img_height) / 2, const.spine_img_width, const.spine_img_height)
        pixmap = pixmap.copy(crop)
        img.setPixmap(pixmap)
        self.layout.addWidget(img)

    def setup_title(self):
        title_label = QtWidgets.QLabel()
        title_label.setFixedWidth(const.spine_img_width)
        title_label.setFixedHeight(50)
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setContentsMargins(0, 0, 0, 0)
        title_label.setPalette(const.highlight_color)
        title_label.setAutoFillBackground(True)
        title_label.setWordWrap(True)
        title_label.setText(self.title)
        titlefont = QFont()
        titlefont.setPointSize(14)
        title_label.setFont(titlefont)
        self.layout.addWidget(title_label)



class BlankSpine(QtWidgets.QFrame):
    """Blank spines to add to the bookshelf to squeeze books into the top left corner
    """
    def __init__(self):
        super().__init__()
        self.setFixedWidth(const.spine_width)
        self.setFixedHeight(const.spine_height)