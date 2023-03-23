# standard libraries
from datetime import datetime
from functools import partial

# dependencies
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QBoxLayout
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QMessageBox

# local modules
import constants as const
from ui.details_frame import Ui_details_panel



'''
TODO:
    - right click menu for
        * remove trait
        * deselect
        * delete
        * add
'''


class CharacterCard(QListWidget):
    def __init__(self, select_signal):
        # select_signal is either details_character_select or search_character_select
        self.select_signal = select_signal
        super().__init__()
        self.setFixedHeight(200)
        self.setAutoFillBackground(True)
        # self.setSortingEnabled(True)
        self.itemDoubleClicked.connect(self.remove_item)

    def select(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Base, const.Colors.HIGHLIGHT)
        self.setPalette(palette)

    def deselect(self):
        self.setPalette(QPalette())

    def remove_item(self):
        self.takeItem(self.currentRow())

    def mousePressEvent(self, e) -> None:
        self.select_signal.emit(self)
        return super().mousePressEvent(e)

    def mouseDoubleClickEvent(self, e) -> None:
        self.remove_item()

    def contextMenuEvent(self, event):
        menu = QMenu()
        delete = menu.addAction('Delete Character')
        if (selection := menu.exec_(event.globalPos())):
            if selection == delete:
                self.setParent(None)





class DetailsPanel(QFrame, Ui_details_panel):
    """Allows for editing information about a book.

    Args:
        db (database.DBHandler)
        signals (signals.Signals)
        book_id (int): ID of the book that this panel is displaying info about. -1 is none selected

    Attributes:
        cover_img (QLabel)
        title_text (QLineEdit)
        artist_text (QLineEdit)
        artist_list (QListWidget)
        series_dropdown (QComboBox)
        order_number (QSpinBox)
        rating_number (QSpinBox)
        pages_text (QLineEdit)
        date_text (QDateEdit)
        genre_text (QLineEdit)
        genre_list (QListWidget)
        tag_text (QLineEdit)
        tag_list (QListWidget)
        notes_text (QTextEdit)
        submit_button (QPushButton)
    """
    def __init__(self, db, signals):
        super().__init__()
        self.setupUi(self)
        self.db = db
        self.signals = signals
        self.book_id = -1
        self.selected_character = None
        self.character_scroll_layout.setDirection(QBoxLayout.BottomToTop)
        self.character_scroll_layout.addStretch()
        self.populate_metadata()
        self.connect_events()



    def populate_metadata(self):
        self.clear_fields()

        metadata = self.db.get_metadata()

        # populate series options
        self.series_dropdown.addItem('')
        for series in metadata['series']:
            self.series_dropdown.addItem(series.text(), series.id_)

        # populate metadata lists
        for artist in metadata['artists']:
            self.artists_list.addItem(artist)
        for genre in metadata['genres']:
            self.genres_list.addItem(genre)
        for tag in metadata['tags']:
            self.tags_list.addItem(tag)
        for trait in metadata['traits']:
            self.traits_list.addItem(trait)



    def connect_events(self):
        # typing in the search bars
        self.artists_text.textChanged.connect(partial(self.search_list, self.artists_list))
        self.genres_text.textChanged.connect(partial(self.search_list, self.genres_list))
        self.tags_text.textChanged.connect(partial(self.search_list, self.tags_list))
        self.traits_text.textChanged.connect(partial(self.search_list, self.traits_list))

        # hitting enter in the search bars
        self.artists_text.returnPressed.connect(partial(self.apply_metadata_text, self.artists_text, self.artists_list))
        self.genres_text.returnPressed.connect(partial(self.apply_metadata_text, self.genres_text, self.genres_list))
        self.tags_text.returnPressed.connect(partial(self.apply_metadata_text, self.tags_text, self.tags_list))
        self.traits_text.returnPressed.connect(partial(self.add_trait_to_character, self.traits_list))

        # double clicking a list item
        self.artists_list.itemDoubleClicked.connect(partial(self.apply_metadata, self.artists_list))
        self.genres_list.itemDoubleClicked.connect(partial(self.apply_metadata, self.genres_list))
        self.tags_list.itemDoubleClicked.connect(partial(self.apply_metadata, self.tags_list))
        self.traits_list.itemDoubleClicked.connect(self.add_trait_to_character)

        # buttons
        self.submit_button.clicked.connect(self.submit)
        self.add_character_button.clicked.connect(self.add_character)

        # signals
        self.signals.populate_details.connect(self.populate_book_info)
        self.signals.depopulate_details.connect(self.cleanse_details)
        self.signals.update_metadata.connect(self.update_metadata)
        self.signals.details_character_select.connect(self.select_character)



    def clear_fields(self):
        self.cover_img.clear()
        self.title_text.clear()
        self.artists_text.clear()
        self.artists_list.clear()
        self.series_dropdown.clear()
        self.order_number.setValue(0)
        self.rating_number.setValue(0)
        self.pages_text.clear()
        self.date_text.clear()
        self.genres_text.clear()
        self.genres_list.clear()
        self.tags_text.clear()
        self.tags_list.clear()
        self.traits_text.clear()
        self.traits_list.clear()
        self.notes_text.clear()
        for i in reversed(range(self.character_scroll_layout.count())):
            if (item := self.character_scroll_layout.itemAt(i).widget()) != None:
                item.setParent(None)



    def update_metadata(self):
        """Updates all the metadata when metadata is edited in any way

        Makes sure to re-populate book info if a book is currently selected
        """
        if self.book_id >= 0:
            cover_img = self.cover_img.pixmap().copy()
        self.populate_metadata()
        if self.book_id >= 0:
            self.populate_book_info(cover_img, self.book_id)



    def populate_book_info(self, cover_img, book_id):
        self.book_id = book_id
        book_info = self.db.get_book_info(book_id)

        self.cover_img.setPixmap(cover_img)
        self.title_text.setText(book_info['name'])
        self.alt_title_text.setText(book_info['alt_name'])
        self.series_dropdown.setCurrentText(book_info['series'].text())
        self.order_number.setValue((0 if not book_info['series_order'] else book_info['series_order']))
        self.rating_number.setValue((0 if not book_info['rating'] else book_info['rating']))
        self.pages_text.setText(str(book_info['pages']))
        self.date_text.setText(datetime.fromisoformat(book_info['date_added']).strftime('%B %d, %Y - %I:%M%p'))
        self.notes_text.setText(book_info['notes'])

        for i in range(self.artists_list.count()):
            item = self.artists_list.item(i)
            if item in book_info['artists']:
                self.apply_metadata(self.artists_list, item)

        for i in range(self.genres_list.count()):
            item = self.genres_list.item(i)
            if item in book_info['genres']:
                self.apply_metadata(self.genres_list, item)

        for i in range(self.tags_list.count()):
            item = self.tags_list.item(i)
            if item in book_info['tags']:
                self.apply_metadata(self.tags_list, item)

        for character_id, traits in book_info['characters'].items():
            character = self.add_character()
            for trait in traits:
                character.addItem(trait)



    def cleanse_details(self):
        """Cleanses info about the currently selected book

        Executed when a book is deselected in the gallery
        """
        self.book_id = -1
        self.selected_character = None
        self.populate_metadata()



    def apply_metadata(self, list_widget, item):
        """Applies or unapplies the selected metadata and sorts the list.

        Changes the applied status to the opposite of what it currently is

        Args:
            list_widget (QListWidget)
            item (ListItem)
        """
        # flip flop the applied status
        if item.background() == const.Colors.AND:
            item.setBackground(const.Colors.NONE)
        elif item.background() == const.Colors.NONE:
            item.setBackground(const.Colors.AND)

        # take out all the items in the list and sort them based on their applied status
        applied = []
        unapplied = []
        while len(list_widget): # remove each item and sort them into their appropriate groups
            item = list_widget.takeItem(0)
            if item.background() == const.Colors.AND:
                applied.append(item)
            elif item.background() == const.Colors.NONE:
                unapplied.append(item)

        # sort backwards (explained below)
        applied.sort(key=lambda x: x.text(), reverse=True)
        unapplied.sort(key=lambda x: x.text(), reverse=True)

        # re-add the items in the correct order
        for item in unapplied: # we add everything in backwards because it's easier to insert each item at pos 0 rather than find out what the last pos is
            list_widget.insertItem(0, item)
        for item in applied:
            list_widget.insertItem(0, item)



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



    def apply_metadata_text(self, text_widget, list_widget):
        """Applies the filter to the topmost ListItem and then floats it to the top of the list

        Alternatively, the user can use prefixes to determine the filter type.
        Executed when a user hits enter in a listwidget's lineedit.

        Args:
            text_widget (QLineEdit)
            list_widget (QListWidget)
        """
        for i in range(list_widget.count()):
            item = list_widget.item(i)
            if not item.isHidden():
                self.apply_metadata(list_widget, item)
                break

        text_widget.clear()



    def add_character(self) -> CharacterCard:
        character = CharacterCard(self.signals.details_character_select)
        character.setSortingEnabled(True)
        self.character_scroll_layout.addWidget(character)
        self.select_character(character)
        return character



    def select_character(self, source: CharacterCard):
        if self.selected_character != None:
            self.selected_character.deselect()
        source.select()
        self.selected_character = source



    def add_trait_to_character(self, trait):
        """adds the specified trait to the currently selected characer

        Args:
            trait (database.ListItem or QListWidget): QListWidget specifies self.traits_list and is triggered by hitting enter in the text box
        """
        if self.selected_character == None:
            return
        if type(trait) == QListWidget:
            for i in range(trait.count()):
                if not trait.item(i).isHidden():
                    copy = trait.item(i).clone()
                    break
        else:
            copy = trait.clone()
        self.selected_character.addItem(copy)



    def submit(self):
        """Updates a book with new information.
        """
        # make sure a book is selected
        if self.book_id < 0:
            return

        # confirm with user that they actually want to edit the book
        popup = QMessageBox()
        popup.setIcon(QMessageBox.Warning)
        popup.setWindowTitle('Confirm')
        popup.setText(f'Are you sure you want to update this manga\'s metadata?')
        popup.setStandardButtons(QMessageBox.Yes | (no := QMessageBox.Cancel))
        response = popup.exec_()

        if response == no:
            return

        # collect data
        data = dict()
        data['id'] = self.book_id
        data['title'] = self.title_text.text()
        data['alt_title'] = self.alt_title_text.text()
        data['series'] = self.series_dropdown.currentData()
        data['series_order'] = (self.order_number.value() if self.order_number.value() else None)
        data['rating'] = (self.rating_number.value() if self.rating_number.value() else None)
        data['notes'] = (self.notes_text.toPlainText() if self.notes_text.toPlainText() else None)

        data['artists'] = []
        for i in range(self.artists_list.count()):
            item = self.artists_list.item(i)
            if item.background() == const.Colors.AND:
                data['artists'].append(item.id_)

        data['genres'] = []
        for i in range(self.genres_list.count()):
            item = self.genres_list.item(i)
            if item.background() == const.Colors.AND:
                data['genres'].append(item.id_)

        data['tags'] = []
        for i in range(self.tags_list.count()):
            item = self.tags_list.item(i)
            if item.background() == const.Colors.AND:
                data['tags'].append(item.id_)

        data['characters'] = []
        for i in range(self.character_scroll_layout.count()):
            character = []
            character_list = self.character_scroll_layout.itemAt(i).widget()
            if character_list == None: # skip the stretch that was added
                continue
            for j in range(character_list.count()):
                trait = character_list.item(j)
                character.append(trait.id_)
            if character:
                data['characters'].append(character)


        # make sure title (required field) is filled
        if not data['title']:
            popup = QMessageBox()
            popup.setIcon(QMessageBox.Critical)
            popup.setWindowTitle('Error')
            popup.setText('Missing title!')
            popup.setStandardButtons(QMessageBox.Close)
            popup.exec_()
            return

        # update info
        self.db.update_book(data)
        self.signals.update_spine.emit(data['id'])

        # inform user of successful operation
        popup = QMessageBox()
        popup.setIcon(QMessageBox.Information)
        popup.setWindowTitle('Success')
        popup.setText(f'{data["title"]} updated successfully')
        popup.setStandardButtons(QMessageBox.Close)
        popup.exec_()



