# standard libraries
from datetime import datetime
from functools import partial

# dependencies
from PyQt5.QtWidgets import QBoxLayout
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QMenu

# local modules
import constants as const
from details_panel import CharacterCard
from ui.search_frame import Ui_search_panel



class SearchFilters:
    def __init__(self, and_list: list[int] = [], not_list: list[int] = [], or_list: list[int] = []):
        self.data = {
            const.Filters.AND: and_list,
            const.Filters.NOT: not_list,
            const.Filters.OR: or_list
        }

    def add(self, filter_type: const.Filters, value: int):
        self.data[filter_type].append(value)

    def has(self, filter_type: const.Filters):
        return bool(self.data[filter_type])

    def get_query_list(self, filter_type: const.Filters):
        return '(' + ','.join(map(str, self.data[filter_type])) + ')'



class SearchPanel(QFrame, Ui_search_panel):
    """Advanced Search

    Attributes:
        filter_prev_button (QPushButton)
        filter_next_button (QPushButton)
        filter_text (QLabel)
        title_text (QLineEdit)
        artists_text (QLineEdit)
        artists_list (QListWidget)
        rating_number (QSpinBox)
        rating_toggle (QCheckBox)
        pages_number_low (QComboBox)
        pages_number_high (QComboBox)
        date_low (QDateEdit)
        date_high (QDateEdit)
        genres_text (QLineEdit)
        genres_list (QListWidget)
        tags_text (QLineEdit)
        tags_list (QListWidget)
        submit_button (QPushButton)
        clear_button (QPushButton)
    """
    def __init__(self, db, signals):
        super().__init__()
        self.db = db
        self.signals = signals
        self.filter_type = const.Filters.AND
        self.selected_character = None
        self.setupUi(self)
        self.character_scroll_layout.setDirection(QBoxLayout.BottomToTop)
        self.character_scroll_layout.addStretch()
        self.connect_events()
        self.populate_metadata()



    def connect_events(self):
        # typing in the search bars
        self.artists_text.textChanged.connect(partial(self.search_list, self.artists_list))
        self.genres_text.textChanged.connect(partial(self.search_list, self.genres_list))
        self.tags_text.textChanged.connect(partial(self.search_list, self.tags_list))
        self.traits_text.textChanged.connect(partial(self.search_list, self.traits_list))

        # hitting enter in the sarch bars
        self.artists_text.returnPressed.connect(partial(self.add_filter_text, self.artists_text, self.artists_list))
        self.genres_text.returnPressed.connect(partial(self.add_filter_text, self.genres_text, self.genres_list))
        self.tags_text.returnPressed.connect(partial(self.add_filter_text, self.tags_text, self.tags_list))
        self.traits_text.returnPressed.connect(partial(self.add_trait_to_character, self.traits_list))

        # double clicking a list item
        self.artists_list.itemDoubleClicked.connect(partial(self.add_filter, self.artists_list))
        self.genres_list.itemDoubleClicked.connect(partial(self.add_filter, self.genres_list))
        self.tags_list.itemDoubleClicked.connect(partial(self.add_filter, self.tags_list))
        self.traits_list.itemDoubleClicked.connect(self.add_trait_to_character)

        # buttons
        self.filter_prev_button.clicked.connect(partial(self.change_filter, -1))
        self.filter_next_button.clicked.connect(partial(self.change_filter, 1))
        self.no_artists_button.clicked.connect(self.toggle_no_artists)
        self.no_genres_button.clicked.connect(self.toggle_no_genres)
        self.no_tags_button.clicked.connect(self.toggle_no_tags)
        self.add_character_button.clicked.connect(self.add_character)
        self.no_characters_button.clicked.connect(self.toggle_no_characters)
        self.submit_button.clicked.connect(self.submit)
        self.clear_button.clicked.connect(self.populate_metadata)

        # right click context menu
        self.date_low.contextMenuEvent = partial(self.context_menu, self.date_low)
        self.date_high.contextMenuEvent = partial(self.context_menu, self.date_high)

        # signals
        self.signals.update_metadata.connect(self.populate_metadata)
        self.signals.clear_filter.connect(self.populate_metadata)
        self.signals.clear_filter.connect(self.submit)
        self.signals.search_character_select.connect(self.select_character)



    def populate_metadata(self):
        self.clear_fields()
        metadata = self.db.get_metadata()

        for item in metadata['artists']:
            self.artists_list.addItem(item)
        for item in metadata['genres']:
            self.genres_list.addItem(item)
        for item in metadata['tags']:
            self.tags_list.addItem(item)
        for item in metadata['traits']:
            self.traits_list.addItem(item)



    def clear_fields(self):
        self.title_text.clear()
        self.no_artists_button.setText('No Artists')
        self.artists_text.clear()
        self.artists_text.setEnabled(True)
        self.artists_list.clear()
        self.artists_list.setEnabled(True)
        self.rating_number.setValue(-1)
        self.rating_toggle.setCheckState(2)
        self.pages_number_low.setValue(0)
        self.pages_number_high.setValue(0)
        self.date_low.setDateTime(self.date_low.minimumDateTime())
        self.date_high.setDateTime(self.date_high.minimumDateTime())
        self.no_genres_button.setText('No Genres')
        self.genres_text.clear()
        self.genres_text.setEnabled(True)
        self.genres_list.clear()
        self.genres_list.setEnabled(True)
        self.no_tags_button.setText('No Tags')
        self.tags_text.clear()
        self.tags_text.setEnabled(True)
        self.tags_list.clear()
        self.tags_list.setEnabled(True)
        self.add_character_button.setEnabled(True)
        self.character_scroll_area.setEnabled(True)
        self.character_scroll_layout.setEnabled(True)
        for index in reversed(range(self.character_scroll_layout.count())):
            item = self.character_scroll_layout.itemAt(index).widget()
            if item != None:
                item.setParent(None)
        self.no_characters_button.setText('No Characters')
        self.traits_text.clear()
        self.traits_list.clear()



    def change_filter(self, index_change):
        """Changes the filter type so you can filter by AND, NOT, OR

        Order for cycling is CLEAR > AND > NOT > OR

        Args:
            index_change (int): how much to cycle forward or backward in the filter type selection
        """
        self.filter_type += index_change
        if self.filter_type < 0:
            self.filter_type = 3
        elif self.filter_type > 3:
            self.filter_type = 0

        text = {
            const.Filters.NONE: ('CLEAR ($)', const.Palettes.CLEANSE),
            const.Filters.AND: ('AND (+, &)', const.Palettes.AND),
            const.Filters.NOT: ('NOT (-, !)', const.Palettes.NOT),
            const.Filters.OR: ('OR (/, |)', const.Palettes.OR)
        }

        self.filter_text.setText(text[self.filter_type][0])
        self.filter_text.setPalette(text[self.filter_type][1])



    def add_filter(self, source, item, filter_type=None):
        """Applies the filter to the selected metadata ListItem and then floats it to the top of the list

        Executed when a user double clicks a list item or after a user hits enter ina listwidget's lineedit

        Args:
            source (QListWidget)
            item (ListItem)
            filter_type (int)
        """
        colors = {
            const.Filters.NONE: const.Colors.NONE,
            const.Filters.AND: const.Colors.AND,
            const.Filters.NOT: const.Colors.NOT,
            const.Filters.OR: const.Colors.OR
        }

        if filter_type is None:
            filter_type = self.filter_type

        if item.background() == colors[filter_type]: # if we're applying a filter that is already applied to this item, reset selection
            filter_type = const.Filters.NONE

        # apply filter to this item
        item.setBackground(colors[filter_type])
        item.filter_type = filter_type


        # take out all the items in the list and re-sort them in a custom order:
        #       AND filters  ->  NOT filters  ->  OR filters  -> no filters
        #       then sort alphabetically in those groups
        sorting_hat = {
            const.Filters.NONE: [],
            const.Filters.OR: [],
            const.Filters.NOT: [],
            const.Filters.AND: []
        }
        while len(source): # remove each item and sort them into their appropriate groups
            temp = source.takeItem(0)
            sorting_hat[temp.filter_type].append(temp)

        for key in sorting_hat:
            # re-add each item in the correct order
            # we add everything in backwards because it's easier to insert each item at pos 0 rather than find out what the last pos is
            sorting_hat[key].sort(key=lambda x: x.text(), reverse=True)
            for element in sorting_hat[key]:
                source.insertItem(0, element)



    def search_list(self, list_widget, search_term):
        """Hides and reveals items in the list widget based on the text being typed in the corresponding line edit

        Args:
            list_widget (QListWidget)
            search_term (str)
        """
        prefixes = '+&-!/|$'
        search_term = search_term.lower()
        if search_term and search_term[0] in prefixes:
            search_term = search_term[1:]
        for i in range(list_widget.count()):
            item = list_widget.item(i)
            if search_term in item.text().lower():
                item.setHidden(False)
            else:
                item.setHidden(True)



    def add_filter_text(self, text_widget, list_widget):
        """Applies the filter to the topmost ListItem and then floats it to the top of the list

        Alternatively, the user can use prefixes to determine the filter type.
        Executed when a user hits enter in a listwidget's lineedit.

        Args:
            text_widget (QLineEdit)
            list_widget (QListWidget)
        """
        filter_type = None
        prefix = text_widget.text()[0]
        if prefix in '+&':
            filter_type = const.Filters.AND
        elif prefix in '-!':
            filter_type = const.Filters.NOT
        elif prefix in '/|':
            filter_type = const.Filters.OR
        elif prefix in '$':
            filter_type = const.Filters.NONE

        for i in range(list_widget.count()):
            item = list_widget.item(i)
            if not item.isHidden():
                self.add_filter(list_widget, item, filter_type)
                break

        text_widget.clear()



    def add_trait_to_character_text(self, text_widget, list_widget):
        filter_type = None
        prefix = text_widget.text()[0]
        if prefix in '+&':
            filter_type = const.Filters.AND
        elif prefix in '-!':
            filter_type = const.Filters.NOT
        elif prefix in '/|':
            filter_type = const.Filters.OR
        elif prefix in '$':
            filter_type = const.Filters.NONE

        for i in range(list_widget.count()):
            item = list_widget.item(i)
            if not item.isHidden():
                self.add_trait_to_character(item, filter_type)
                break

        text_widget.clear()



    def add_trait_to_character(self, trait, filter_type = None):
        # clone the trait item
        if self.selected_character == None:
            return
        if type(trait) == QListWidget:
            for i in range(trait.count()):
                if not trait.item(i).isHidden():
                    copy = trait.item(i).clone()
                    break
        else:
            copy = trait.clone()

        # apply filter to cloned item
        colors = {
            const.Filters.AND: const.Colors.AND,
            const.Filters.NOT: const.Colors.NOT,
            const.Filters.OR: const.Colors.OR
        }

        if filter_type is None:
            filter_type = self.filter_type

        copy.setBackground(colors[filter_type])
        copy.filter_type = filter_type

        # don't add duplicate traits
        # if trait is already in list, change filter type if necessary
        for i in range(self.selected_character.count()):
            trait = self.selected_character.item(i)
            if copy == trait:
                if copy.filter_type == trait.filter_type:
                    return
                else:
                    self.selected_character.takeItem(i)
                    break
        self.selected_character.addItem(copy)

        # take out all the items in the list and re-sort them in a custom order:
        #       AND filters  ->  NOT filters  ->  OR filters
        #       then sort alphabetically in those groups
        sorting_hat = {
            const.Filters.OR: [],
            const.Filters.NOT: [],
            const.Filters.AND: []
        }
        while len(self.selected_character): # remove each item and sort them into their appropriate groups
            temp = self.selected_character.takeItem(0)
            sorting_hat[temp.filter_type].append(temp)

        for key in sorting_hat:
            # re-add each item in the correct order
            # we add everything in backwards because it's easier to insert each item at pos 0 rather than find out what the last pos is
            sorting_hat[key].sort(key=lambda x: x.text(), reverse=True)
            for element in sorting_hat[key]:
                self.selected_character.insertItem(0, element)



    def toggle_no_artists(self):
        if self.artists_text.isEnabled():
            self.artists_text.setEnabled(False)
            self.artists_list.setEnabled(False)
            self.no_artists_button.setText('Search Artists')
        else:
            self.artists_text.setEnabled(True)
            self.artists_list.setEnabled(True)
            self.no_artists_button.setText('No Artists')



    def toggle_no_genres(self):
        if self.genres_text.isEnabled():
            self.genres_text.setEnabled(False)
            self.genres_list.setEnabled(False)
            self.no_genres_button.setText('Search Genres')
        else:
            self.genres_text.setEnabled(True)
            self.genres_list.setEnabled(True)
            self.no_genres_button.setText('No Genres')



    def toggle_no_tags(self):
        if self.tags_text.isEnabled():
            self.tags_text.setEnabled(False)
            self.tags_list.setEnabled(False)
            self.no_tags_button.setText('Search Tags')
        else:
            self.tags_text.setEnabled(True)
            self.tags_list.setEnabled(True)
            self.no_tags_button.setText('No Tags')



    def toggle_no_characters(self):
        if self.add_character_button.isEnabled():
            self.add_character_button.setEnabled(False)
            self.character_scroll_area.setEnabled(False)
            self.character_scroll_layout.setEnabled(False)
            self.no_characters_button.setText('Search Characters')
        else:
            self.add_character_button.setEnabled(True)
            self.character_scroll_area.setEnabled(True)
            self.character_scroll_layout.setEnabled(True)
            self.no_characters_button.setText('No Characters')



    def select_character(self, source: CharacterCard):
        if self.selected_character != None:
            self.selected_character.deselect()
        source.select()
        self.selected_character = source



    def add_character(self):
        character = CharacterCard(self.signals.search_character_select)
        self.character_scroll_layout.addWidget(character)
        self.select_character(character)



    def submit(self):
        """Stores all the form information into a dict and then emits a signal to apply the search filters
        """
        list_picker = {
            self.artists_list: 'artists',
            self.genres_list: 'genres',
            self.tags_list: 'tags'
        }

        filters = {
            'basic': {
                'title': self.title_text.text(),
                'rating': (self.rating_number.value(), self.rating_toggle.checkState()),
                'pages_low': self.pages_number_low.value(),
                'pages_high': self.pages_number_high.value(),
                'date_low': self.date_low.dateTime().toPyDateTime(),
                'date_high':self.date_high.dateTime().toPyDateTime(),
            }
        }

        for list_ in list_picker.keys():
            if not list_.isEnabled():
                continue
            data = {
                const.Filters.AND: [],
                const.Filters.NOT: [],
                const.Filters.OR: []
            }
            for i in range(list_.count()):
                item = list_.item(i)
                if item.filter_type == 0:
                    continue
                data[item.filter_type].append(item.id_)
            filters[list_picker[list_]] = SearchFilters(data[const.Filters.AND], data[const.Filters.NOT], data[const.Filters.OR])

        # characters are special and need different logic than the other fields
        if self.add_character_button.isEnabled():
            filters['characters'] = []
            for index in range(self.character_scroll_layout.count()):
                character = self.character_scroll_layout.itemAt(index).widget()
                if character == None:
                    continue
                data = {
                    const.Filters.AND: [],
                    const.Filters.NOT: [],
                    const.Filters.OR: []
                }
                for index in range(character.count()):
                    trait = character.item(index)
                    if trait.filter_type == 0:
                        continue
                    data[trait.filter_type].append(trait.id_)
                filters['characters'].append(SearchFilters(data[const.Filters.AND], data[const.Filters.NOT], data[const.Filters.OR]))

        self.signals.search_advanced.emit(filters)
        self.signals.show_bookshelf_panel.emit()



    def context_menu(self, source, event):
        """Opens a context menu for the dates because properly setting / resetting them can be annoying

        "Reset This Date": resets the date back to default
        "Set To Now": sets this date to now

        Args:
            event (QMouseEvent): The event that was emitted. Unused, but required by PyQt5
        """
        menu = QMenu()
        clear_selected = menu.addAction('Reset This Date')
        set_now = menu.addAction('Set To Now')
        if (selection := menu.exec_(event.globalPos())):
            if selection == clear_selected:
                source.setDateTime(source.minimumDateTime())
            elif selection == set_now:
                source.setDateTime(datetime.now())