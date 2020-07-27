# standard libraries
from functools import partial

# dependencies
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QMessageBox

# local modules
from ui.metadata_frame import Ui_metadata_panel
import exceptions



class MetadataPanel(QFrame, Ui_metadata_panel):
    """Controls adding and deleting metadata entries.

    Args:
        metadata (metadata.Data)
        signals (signals.Signals)

    Attributes:
        metadata (metadata.Data)
        siganls (signals.Signals)

        artists_text (QLineEdit)
        artists_submit (QPushButton)
        artists_list (QListWidget)
        series_text (QLineEdit)
        series_submit (QPushButton)
        series_list (QListWidget)
        genres_text (QLineEdit)
        genres_submit (QPushButton)
        genres_list (QListWidget)
        tags_text (QLineEdit)
        tags_submit (QPushButton)
        tags_list (QListWidget)
    """
    def __init__(self, metadata, signals):
        super().__init__()
        self.setupUi(self)
        self.metadata = metadata
        self.signals = signals
        self.connect_events()



    def connect_events(self):
        # submit buttons
        self.artists_submit.clicked.connect(partial(self.create_entry, self.artists_text))
        self.series_submit.clicked.connect(partial(self.create_entry, self.series_text))
        self.genres_submit.clicked.connect(partial(self.create_entry, self.genres_text))
        self.tags_submit.clicked.connect(partial(self.create_entry, self.tags_text))

        # pressing enter in line edits (has the same functionality as the submit button)
        self.artists_text.returnPressed.connect(partial(self.create_entry, self.artists_text))
        self.series_text.returnPressed.connect(partial(self.create_entry, self.series_text))
        self.genres_text.returnPressed.connect(partial(self.create_entry, self.genres_text))
        self.tags_text.returnPressed.connect(partial(self.create_entry, self.tags_text))

        # right click context menu
        self.artists_list.contextMenuEvent = partial(self.context_menu, self.artists_list)
        self.series_list.contextMenuEvent = partial(self.context_menu, self.series_list)
        self.genres_list.contextMenuEvent = partial(self.context_menu, self.genres_list)
        self.tags_list.contextMenuEvent = partial(self.context_menu, self.tags_list)

        # update lists
        self.signals.update_metadata.connect(self.populate_lists)



    def create_entry(self, text_area, event=None):
        """Attempts to create a new metadata entry.

        If an entry with that name already exists, display an error popup window.

        Args:
            text_area (QLineEdit)
            event (QEvent, optional): needs to be optional because text_area.returnPressed signal does not send an event
        """
        try:
            if text_area.text():
                table = text_area.objectName()[:-5]
                self.metadata.create(table, text_area.text())
                text_area.clear()
        except exceptions.DuplicateEntry:
            popup = QMessageBox()
            popup.setIcon(QMessageBox.Critical)
            popup.setWindowTitle('Error')
            popup.setText('Unable to add that metadata entry.')
            popup.setInformativeText(f'"{text_area.text()}" is already an existing metadata entry.')
            popup.setStandardButtons(QMessageBox.Close)
            popup.exec_()



    def context_menu(self, source, event):
        """Opens a context menu for the books.

        "Clear Selected": clears the selected list items
        "Delete": deletes the metadata entry after a confirmation message

        Args:
            event (QMouseEvent): The event that was emitted. Unused, but required by PyQt5
        """
        menu = QMenu()
        clear = menu.addAction('Clear Selected')
        delete = menu.addAction('Delete')

        if (selection := menu.exec_(event.globalPos())):
            if selection == clear:
                source.clearSelection()
            elif selection == delete:
                if (selected := source.currentItem()): # only proceed if the user has selected something to delete
                    # confirmation popup
                    popup = QMessageBox()
                    popup.setIcon(QMessageBox.Warning)
                    popup.setWindowTitle('Confirm')
                    popup.setText(f'Are you sure you want to delete {selected.text()}?')
                    popup.setStandardButtons((yes := QMessageBox.Yes) | QMessageBox.Cancel)
                    response = popup.exec_()

                    if response == yes:
                        self.metadata.delete(selected)



    def populate_lists(self):
        """Populates each of the lists
        """
        self.artists_list.clear()
        self.series_list.clear()
        self.genres_list.clear()
        self.tags_list.clear()
        for item in self.metadata.mdata:
            if item.table == 'artists':
                self.artists_list.addItem(item)
            elif item.table == 'series':
                self.series_list.addItem(item)
            elif item.table == 'genres':
                self.genres_list.addItem(item)
            elif item.table == 'tags':
                self.tags_list.addItem(item)