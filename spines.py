# standard libraries
from os import listdir

# dependencies
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QFont

# local modules
import constants as const



class BookSpine(QtWidgets.QFrame):
    """Custom QFrame object to display in the bookshelf

    Done this way partially to abstract away the frame creation, but mainly to hold instance variables

    Args:
        book_id (int)
        title (str): the title of the book
        folder (str): the base directory of all the books. NOT the directory of this specific book.

    Attributes:
        title (str)
        layout (QVBoxLayout)
    """
    def __init__(self, book_id: int, title: str, folder: str):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout()
        self.id_ = book_id
        self.title = title
        self.folder = folder
        self.image = None
        self.loaded_image = None
        self.scale = QtWidgets.QDesktopWidget().screenGeometry(0).width() / 1920

        self.setup_frame()
        self.setup_layout()
        self.setup_img()
        self.setup_title()

    def setup_frame(self):
        self.setFixedWidth(int(const.Spines.WIDTH * self.scale))
        self.setFixedHeight(int(const.Spines.HEIGHT * self.scale))
        self.setFrameShape(QtWidgets.QFrame.Box)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.setContentsMargins(3, 3, 3, 3)
        self.setPalette(const.Palettes.PRIMARY)
        self.setAutoFillBackground(True)

    def setup_layout(self):
        self.layout.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)
        self.setLayout(self.layout)

    def setup_img(self):
        self.image = QtWidgets.QLabel()
        self.image.setFixedWidth(int(const.Spines.IMG_WIDTH * self.scale))
        self.image.setFixedHeight(int(const.Spines.IMG_HEIGHT * self.scale))
        self.image.setAlignment(QtCore.Qt.AlignCenter)
        self.image.setContentsMargins(0, 0, 0, 0)
        self.loaded_image = QPixmap(f'{const.directory}/{self.folder}/{listdir(f"{const.directory}/{self.folder}/")[0]}')
        img = self.loaded_image.scaledToWidth(int(const.Spines.IMG_WIDTH * self.scale), QtCore.Qt.SmoothTransformation)
        crop = QtCore.QRect((img.width() - int(const.Spines.IMG_WIDTH * self.scale)) / 2, (img.height() - int(const.Spines.IMG_HEIGHT * self.scale)) / 2, int(const.Spines.IMG_WIDTH * self.scale), int(const.Spines.IMG_HEIGHT * self.scale))
        img = img.copy(crop)
        self.image.setPixmap(img)
        self.layout.addWidget(self.image)

    def setup_title(self):
        self.title_label = QtWidgets.QLabel()
        self.title_label.setFixedWidth(int(const.Spines.IMG_WIDTH * self.scale))
        self.title_label.setFixedHeight(50)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setContentsMargins(0, 0, 0, 0)
        self.title_label.setPalette(const.Palettes.SECONDARY)
        self.title_label.setAutoFillBackground(True)
        self.title_label.setWordWrap(True)
        self.title_label.setText(self.title)
        titlefont = QFont()
        titlefont.setPointSize(14)
        self.title_label.setFont(titlefont)
        self.layout.addWidget(self.title_label)

    def update_title(self, title: str):
        self.title = title
        self.title_label.setText(self.title)

    def resize(self, window_width: int):
        self.scale = window_width / 1920
        self.setup_frame()

        self.image.setFixedWidth(int(const.Spines.IMG_WIDTH * self.scale))
        self.image.setFixedHeight(int(const.Spines.IMG_HEIGHT * self.scale))
        img = self.loaded_image.scaledToWidth(int(const.Spines.IMG_WIDTH * self.scale), QtCore.Qt.SmoothTransformation)
        crop = QtCore.QRect((img.width() - int(const.Spines.IMG_WIDTH * self.scale)) / 2, (img.height() - int(const.Spines.IMG_HEIGHT * self.scale)) / 2, int(const.Spines.IMG_WIDTH * self.scale), int(const.Spines.IMG_HEIGHT * self.scale))
        img = img.copy(crop)
        self.image.setPixmap(img)

        self.title_label.setFixedWidth(int(const.Spines.IMG_WIDTH * self.scale))

    def __eq__(self, compare):
        if isinstance(compare, BookSpine) and self.id_ == compare.id_:
            return True
        return False



class BlankSpine(QtWidgets.QFrame):
    """Blank spines to add to the bookshelf to squeeze books into the top left corner
    """
    def __init__(self):
        super().__init__()
        self.setFixedWidth(const.Spines.WIDTH)
        self.setFixedHeight(const.Spines.HEIGHT)