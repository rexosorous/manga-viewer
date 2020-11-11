# standard libraries
from functools import partial

# dependencies
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QFrame

# local modules
import constants as const
from ui.search_frame import Ui_search_panel



class SearchPanel(QFrame, Ui_search_panel):
    """Advanced Search

    Attributes:
        filter_prev_button (QPushButton)
        filter_next_button (QPushButton)
        filter_text (QLabel)
        title_text (QLineEdit)
        artists_text (QLineEdit)
        artists_list (QListWidget)
        series_text (QLineEdit)
        series_list (QListWidget)
        order_number (QSpinBox)
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
        self.filter_type = const.FILTER_AND
        self.setupUi(self)
        self.connect_events()
        self.populate_lists()



    def connect_events(self):
        self.filter_prev_button.clicked.connect(partial(self.change_filter, -1))
        self.filter_next_button.clicked.connect(partial(self.change_filter, 1))
        self.artists_list.itemDoubleClicked.connect(partial(self.add_filter, self.artists_list))
        self.series_list.itemDoubleClicked.connect(partial(self.add_filter, self.series_list))
        self.genres_list.itemDoubleClicked.connect(partial(self.add_filter, self.genres_list))
        self.tags_list.itemDoubleClicked.connect(partial(self.add_filter, self.tags_list))
        self.submit_button.clicked.connect(self.submit)
        self.clear_button.clicked.connect(self.populate_lists)
        self.signals.update_metadata.connect(self.populate_lists)



    def populate_lists(self):
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



    def clear_fields(self):
        self.title_text.clear()
        self.artists_text.clear()
        self.artists_list.clear()
        self.series_text.clear()
        self.series_list.clear()
        self.order_number.setValue(0)
        self.rating_number.setValue(0)
        self.rating_toggle.setCheckState(2)
        self.pages_number_low.setValue(0)
        self.pages_number_high.setValue(0)
        self.date_low.setDate(QDate(1, 1, 1))
        self.date_high.setDate(QDate(1, 1, 1))
        self.genres_text.clear()
        self.genres_list.clear()
        self.tags_text.clear()
        self.tags_list.clear()



    def change_filter(self, index_change):
        """Changes the filter type so you can filter by AND, NOT, OR

        Order for cycling is CLEAR > AND > NOT > OR

        Args:
            index_change (int): how much to cycle forward or backward in the filter type selection
        """
        self.filter_type += index_change
        if self.filter_type < 0:
            self.filter_type = 0
        elif self.filter_type > 3:
            self.filter_type = 3

        text = {
            0: ('CLEAR', const.cleanse_palette),
            1: ('(+, &) AND', const.and_palette),
            2: ('(-, !) NOT', const.not_palette),
            3: ('(/, |) OR', const.or_palette)
        }

        self.filter_text.setText(text[self.filter_type][0])
        self.filter_text.setPalette(text[self.filter_type][1])



    def add_filter(self, source, item):
        """Applies the filter to the selected metadata ListItem and then floats it to the top of the list

        Args:
            source (QListWidget)
            item (ListItem)
        """
        colors = {
            const.FILTER_NONE: const.no_color,
            const.FILTER_AND: const.and_color,
            const.FILTER_NOT: const.not_color,
            const.FILTER_OR: const.or_color
        }

        if item.background() == colors[self.filter_type]: # if we're applying a filter that is already applied to this item
            return

        # apply filter to this item
        item.setBackground(colors[self.filter_type])
        item.filter_type = self.filter_type


        # take out all the items in the list and re-sort them in a custom order:
        #       AND filters  ->  NOT filters  ->  OR filters  -> no filters
        #       then sort alphabetically in those groups
        sorting_hat = {
            const.FILTER_NONE: [],
            const.FILTER_OR: [],
            const.FILTER_NOT: [],
            const.FILTER_AND: []
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



    def submit(self):
        """Builds a SQLite3 query from the filters chosen by the user and then updates the gallery.

        After building the query, emit a signal so that home.populate_gallery() can handle everything with the gallery and sorting
        """
        where = []

        # text
        if (title := self.title_text.text()):
            where.append(f'(books.name LIKE "%{title}%" OR books.alt_name LIKE "%{title}%")')

        # spinbox
        if (order := self.order_number.value()):
            where.append(f'books.series_order={order}')
        if (rating := self.rating_number.value()):
            if self.rating_toggle.checkState() == 2:
                where.append(f'books.rating>={rating}')
            else:
                where.append(f'books.rating={rating}')
        if (pages_low := self.pages_number_low.value()):
            where.append(f'books.pages>{pages_low}')
        if (pages_high := self.pages_number_high.value()):
            where.append(f'books.pages<{pages_high}')

        # date
        if (date_low := self.date_low.dateTime().toSecsSinceEpoch()) > -6857193600:
            where.append(f'books.date_added>{date_low}')
        if (date_high := self.date_high.dateTime().toSecsSinceEpoch()) > -6857193600:
            where.append(f'books.date_added<{date_high}')

        # list
        list_filters = {
            const.FILTER_AND: [],
            const.FILTER_NOT: [],
            const.FILTER_OR: []
        }

        for i in range(self.artists_list.count()):
            item = self.artists_list.item(i)
            if item.filter_type == 0:
                continue
            list_filters[item.filter_type].append(f'artists.id={item.id_}')

        for i in range(self.series_list.count()):
            item = self.series_list.item(i)
            if item.filter_type == 0:
                continue
            list_filters[item.filter_type].append(f'books.series={item.id_}')

        for i in range(self.genres_list.count()):
            item = self.genres_list.item(i)
            if item.filter_type == 0:
                continue
            list_filters[item.filter_type].append(f'genres.id={item.id_}')

        for i in range(self.tags_list.count()):
            item = self.tags_list.item(i)
            if item.filter_type == 0:
                continue
            list_filters[item.filter_type].append(f'tags.id={item.id_}')

        list_filters[const.FILTER_AND] = ' AND '.join(list_filters[const.FILTER_AND])
        list_filters[const.FILTER_NOT] = ' AND '.join(list_filters[const.FILTER_NOT])
        list_filters[const.FILTER_OR] = ' OR '.join(list_filters[const.FILTER_OR])

        if list_filters[const.FILTER_NOT]:
            list_filters[const.FILTER_NOT] = list_filters[const.FILTER_NOT].replace('=', '!=')
        if list_filters[const.FILTER_OR]:
            list_filters[const.FILTER_OR] = '(' + list_filters[const.FILTER_OR] + ')'

        if (list_filters := ' AND '.join([x for x in list_filters.values() if x])):
            where.append(list_filters) # make sure not to join empty strings together
        where = ' AND '.join(where)

        query = '''
            SELECT DISTINCT books.id, books.name, books.directory
            FROM books
            LEFT JOIN books_artists
            ON books_artists.bookID=books.id
            LEFT JOIN artists
            ON books_artists.artistID=artists.id
            LEFT JOIN series
            ON series.id=books.series
            LEFT JOIN books_genres
            ON books_genres.bookID=books.id
            LEFT JOIN genres
            ON books_genres.genreID=genres.id
            LEFT JOIN books_tags
            ON books_tags.bookID=books.id
            LEFT JOIN tags
            ON books_tags.tagID=tags.id
            WHERE ''' + where

        if not where:
            self.signals.filter_signal.emit('SELECT id, name, directory FROM books')
        else:
            self.signals.filter_signal.emit(query)