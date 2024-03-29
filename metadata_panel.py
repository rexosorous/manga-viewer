# standard libraries
from functools import partial

# dependencies
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QTextEdit

# local modules
import exceptions
from ui.metadata_frame import Ui_metadata_panel



class MetadataPanel(QFrame, Ui_metadata_panel):
    """Controls adding and deleting metadata entries.

    Args:
        db (database.DBHandler)
        signals (signals.Signals)

    Attributes:
        db (database.DBHandler)
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
    def __init__(self, db, signals):
        super().__init__()
        self.setupUi(self)
        self.db = db
        self.signals = signals
        self.connect_events()
        self.populate_metadata()



    def connect_events(self):
        # submit buttons
        self.artists_submit.clicked.connect(partial(self.create_metadata, self.artists_text))
        self.series_submit.clicked.connect(partial(self.create_metadata, self.series_text))
        self.genres_submit.clicked.connect(partial(self.create_metadata, self.genres_text))
        self.tags_submit.clicked.connect(partial(self.create_metadata, self.tags_text))
        self.traits_submit.clicked.connect(partial(self.create_metadata, self.traits_text))

        # typing in the search bars
        self.artists_text.textChanged.connect(partial(self.search_list, self.artists_list))
        self.genres_text.textChanged.connect(partial(self.search_list, self.genres_list))
        self.tags_text.textChanged.connect(partial(self.search_list, self.tags_list))
        self.traits_text.textChanged.connect(partial(self.search_list, self.traits_list))

        # pressing enter in line edits (has the same functionality as the submit button)
        self.artists_text.returnPressed.connect(partial(self.create_metadata, self.artists_text))
        self.series_text.returnPressed.connect(partial(self.create_metadata, self.series_text))
        self.genres_text.returnPressed.connect(partial(self.create_metadata, self.genres_text))
        self.tags_text.returnPressed.connect(partial(self.create_metadata, self.tags_text))
        self.traits_text.returnPressed.connect(partial(self.create_metadata, self.traits_text))

        # right click context menu
        self.artists_list.contextMenuEvent = partial(self.context_menu, self.artists_list)
        self.series_list.contextMenuEvent = partial(self.context_menu, self.series_list)
        self.genres_list.contextMenuEvent = partial(self.context_menu, self.genres_list)
        self.tags_list.contextMenuEvent = partial(self.context_menu, self.tags_list)
        self.traits_list.contextMenuEvent = partial(self.context_menu, self.traits_list)

        # signals
        self.signals.update_metadata.connect(self.populate_metadata)



    def populate_metadata(self):
        """Populates each of the lists
        """
        self.clear_fields()
        metadata = self.db.get_metadata()

        for item in metadata['artists']:
            self.artists_list.addItem(item)
        for item in metadata['series']:
            self.series_list.addItem(item)
        for item in metadata['genres']:
            self.genres_list.addItem(item)
        for item in metadata['tags']:
            self.tags_list.addItem(item)
        for item in metadata['traits']:
            self.traits_list.addItem(item)



    def clear_fields(self):
        self.artists_list.clear()
        self.series_list.clear()
        self.genres_list.clear()
        self.tags_list.clear()
        self.traits_list.clear()



    def search_list(self, list_widget, search_term):
        """Hides and reveals items in the list widget based on the text being typed in the corresponding line edit

        Args:
            list_widget (QListWidget)
            search_term (str)
        """
        search_term = search_term.lower()
        for i in range(list_widget.count()):
            item = list_widget.item(i)
            if search_term in item.text().lower():
                item.setHidden(False)
            else:
                item.setHidden(True)



    def create_metadata(self, text_area, event=None):
        """Attempts to create a new metadata entry.

        If an entry with that name already exists, display an error popup window.

        Args:
            text_area (QLineEdit)
            event (QEvent, optional): needs to be optional because text_area.returnPressed signal does not send an event
        """
        try:
            if text_area.text():
                table = text_area.objectName()[:-5]
                self.db.create_metadata(table, text_area.text())
                text_area.clear()
                self.signals.update_metadata.emit()
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
        "Rename": renames the metadata entry
        "Edit Description": allows for changing the secondary attribute of the table (either description or alt_name)
        "Delete": deletes the metadata entry after a confirmation message

        Args:
            event (QMouseEvent): The event that was emitted. Unused, but required by PyQt5
        """
        menu = QMenu()
        clear = menu.addAction('Clear Selected')
        rename = menu.addAction('Rename')
        edit_description = menu.addAction('Edit Description')
        delete = menu.addAction('Delete')

        if (selection := menu.exec_(event.globalPos())):
            if selection == clear:
                source.clearSelection()
            elif selection == rename:
                if (selected := source.currentItem()): # only proceed if the user has selected something to rename
                    new_description = ''
                    yes_button = True
                    while yes_button and not new_description:
                        new_description, yes_button = QInputDialog.getText(self, 'Rename', f'What would you like "{selected.text()}" to be renamed to?', QLineEdit.Normal, '')

                        if not yes_button:
                            return

                        elif yes_button and new_description:
                            self.db.rename_metadata(selected.table, selected.id_, new_description)
                            self.signals.update_metadata.emit()
                            return

                        popup = QMessageBox()
                        popup.setIcon(QMessageBox.Critical)
                        popup.setWindowTitle('Error')
                        popup.setText('Error\nNo new name specified.')
                        popup.setStandardButtons(QMessageBox.Close)
                        response = popup.exec_()
            elif selection == edit_description:
                if (selected := source.currentItem()): # only proceed if the user has selected something to rename
                    new_description = ''
                    yes_button = True
                    while yes_button and not new_description:
                        new_description, yes_button = QInputDialog.getMultiLineText(self, 'Description', f'What would you like the description for "{selected.text()}" to be?', selected.description)

                        if not yes_button:
                            return

                        elif yes_button and new_description:
                            self.db.update_metadata_description(selected.table, selected.id_, new_description)
                            self.signals.update_metadata.emit()
                            return

                        popup = QMessageBox()
                        popup.setIcon(QMessageBox.Critical)
                        popup.setWindowTitle('Error')
                        popup.setText('Error\nNo new name specified.')
                        popup.setStandardButtons(QMessageBox.Close)
                        response = popup.exec_()
            elif selection == delete:
                if (selected := source.currentItem()): # only proceed if the user has selected something to delete
                    # confirmation popup
                    popup = QMessageBox()
                    popup.setIcon(QMessageBox.Warning)
                    popup.setWindowTitle('Confirm')
                    popup.setText(f'Are you sure you want to delete {selected.text()}?')
                    popup.setStandardButtons(QMessageBox.Yes | (no := QMessageBox.Cancel))
                    response = popup.exec_()

                    if response == no:
                        return

                    self.db.delete_metadata(selected.table, selected.id_)
                    self.signals.update_metadata.emit()