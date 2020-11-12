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
        join_block = []
        where_block = []
        group_block = []
        except_block = ''
        or_block = ''

        # text
        if (title := self.title_text.text()):
            where_block.append(f'(books.name LIKE "%{title}%" OR books.alt_name LIKE "%{title}%")')

        # spinbox
        if (order := self.order_number.value()):
            where_block.append(f'books.series_order={order}')
        if (rating := self.rating_number.value()):
            if self.rating_toggle.checkState() == 2:
                where_block.append(f'books.rating>={rating}')
            else:
                where_block.append(f'books.rating={rating}')
        if (pages_low := self.pages_number_low.value()):
            where_block.append(f'books.pages>={pages_low}')
        if (pages_high := self.pages_number_high.value()):
            where_block.append(f'books.pages<={pages_high}')

        # date
        if (date_low := self.date_low.dateTime().toSecsSinceEpoch()) > -6857193600:
            where_block.append(f'books.date_added>={date_low}')
        if (date_high := self.date_high.dateTime().toSecsSinceEpoch()) > -6857193600:
            where_block.append(f'books.date_added<={date_high}')


        # lists
        list_filters = {
            'artists': {
                const.FILTER_AND: [],
                const.FILTER_NOT: [],
                const.FILTER_OR: []
            },
            'series': {
                const.FILTER_AND: [],
                const.FILTER_NOT: [],
                const.FILTER_OR: []
            },
            'genres': {
                const.FILTER_AND: [],
                const.FILTER_NOT: [],
                const.FILTER_OR: []
            },
            'tags': {
                const.FILTER_AND: [],
                const.FILTER_NOT: [],
                const.FILTER_OR: []
            }
        }

        for i in range(self.artists_list.count()):
            item = self.artists_list.item(i)
            if item.filter_type == 0:
                continue
            list_filters['artists'][item.filter_type].append(f'artistID={item.id_}')

        for i in range(self.series_list.count()):
            item = self.series_list.item(i)
            if item.filter_type == 0:
                continue
            list_filters['series'][item.filter_type].append(f'books.series={item.id_}')

        for i in range(self.genres_list.count()):
            item = self.genres_list.item(i)
            if item.filter_type == 0:
                continue
            list_filters['genres'][item.filter_type].append(f'genreID={item.id_}')

        for i in range(self.tags_list.count()):
            item = self.tags_list.item(i)
            if item.filter_type == 0:
                continue
            list_filters['tags'][item.filter_type].append(f'tagID={item.id_}')

        # build join statements
        if [x for x in list_filters['artists'].values() if x]:
            join_block.append('LEFT JOIN books_artists ON books_artists.bookID=books.id')
        if [x for x in list_filters['genres'].values() if x]:
            join_block.append('LEFT JOIN books_genres ON books_genres.bookID=books.id')
        if [x for x in list_filters['tags'].values() if x]:
            join_block.append('LEFT JOIN books_tags ON books_tags.bookID=books.id')


        # build OR statements
        all_OR = []
        for key in list_filters:
            if (data := list_filters[key][const.FILTER_OR]):
                all_OR += (data)
        all_OR = '\n\tOR '.join(all_OR)
        if all_OR:
            or_block = all_OR


        # build AND statements
        col_picker = {
            'artists': 'artistID',
            'series': 'books.series',
            'genres': 'genreID',
            'tags': 'tagID'
        }
        for key in list_filters:
            if (data := list_filters[key][const.FILTER_AND]):
                count = len(data)
                statements = ('\n\t\t\tOR '.join(data))
                if count > 1:
                    statements = '(\n\t\t\t' + statements + '\n\t\t)'
                    group_block.append(f'COUNT(DISTINCT {col_picker[key]})={count}')
                where_block.append(statements)


        # build NOT statements
        all_NOT = []
        for key in list_filters:
            if (data := list_filters[key][const.FILTER_NOT]):
                all_NOT += (data)
        all_NOT = '\n\t\t\tOR '.join(all_NOT)
        if all_NOT:
            all_NOT = '(\n\t\t\t' + all_NOT + '\n\t\t)'
            except_block = all_NOT


        # convert blocks to strings
        join_string = '\n\t'.join(join_block)
        where_string = '\n\t\tAND '.join(where_block)
        group_string = '\n\t\tAND '.join(group_block)
        except_string = except_block
        or_string = or_block

        # format the strings
        if join_string:
            join_string = join_string + '\n\t'
        if where_string:
            where_string = 'WHERE\n\t\t' + where_string + '\n\t'
        if group_string:
            group_string = 'GROUP BY books.id\n\tHAVING\n\t\t' + group_string + '\n\t'
        if except_string:
            except_string = 'EXCEPT\n\t\tSELECT DISTINCT books.id, books.name, books.directory FROM books\n\t\t' + '\n\t\t'.join(join_block) + '\n\t\tWHERE ' + except_string


        # check to see if there are even any search filters applied
        if not where_block and not except_block and not or_block:
            # send a default query that gets all books if there are no search filters applied
            self.signals.filter_signal.emit('SELECT id, name, directory FROM books')
            return


        # build query
        query = '\tSELECT DISTINCT books.id, books.name, books.directory FROM books\n\t' + join_string + where_string + group_string + except_string
        if or_string:
            query = 'SELECT DISTINCT books.id, books.name, books.directory FROM books INNER JOIN (\n' + query + ') AS temp ON temp.id=books.id\n' + '\n'.join(join_block) + '\nWHERE\n\t' + or_string

        self.signals.filter_signal.emit(query)