# standard libraries
import sqlite3

# dependencies
from PyQt5.QtWidgets import QListWidgetItem

# local modules
import constants as const
from datetime import datetime
import exceptions



class ListItem(QListWidgetItem):
    """ListWidgetItems used to populate the various metadata lists

    This class allows us to store additional information (namely id) to be used in conjunction with the dbhandler to avoid string matching

    Args:
        id_ (int): id of the metadata
        name (str): name of the metadata and what is displayed in the list
        table (str): one of ['artists', 'series', 'genres', 'tags']

    Attributes:
        id_ (int)
        table (str)
    """
    def __init__(self, id_: int, name: str, table: str):
        super().__init__()
        self.id_ = id_
        self.table = table
        self.filter_type = const.Filters.NONE
        self.setText(name)

    def clone(self):
        return ListItem(self.id_, self.text(), self.table)

    def __eq__(self, compare):
        if self.id_ == compare.id_:
            return True
        return False



class DBHandler:
    """Controls connection and all interaction with the database.

    Attributes:
        conn (sqlite3.Connection)
        db (sqlite3.Cursor)
    """
    def __init__(self):
        self.conn = sqlite3.connect('mangalibrary.db')
        self.db = self.conn.cursor()
        self.create_tables()
        self.db.row_factory = self.dict_factory



    def create_tables(self):
        """Initializes the database if lost, deleted, or otherwise missing.
        """
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS books
            (
                id INTEGER PRIMARY KEY,
                date_added DATETIME DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'LOCALTIME')),
                name TEXT,
                alt_name TEXT,
                series INTEGER,
                series_order REAL,
                pages INTEGER,
                rating INTEGER,
                notes TEXT,
                directory TEXT,
                zoom REAL,
                bookmark INTEGER -- the page you left on when you closed the reader
            )
        ''')

        self.db.execute('''
            CREATE TABLE IF NOT EXISTS artists
            (
                id INTEGER PRIMARY KEY,
                name TEXT,
                alt_name TEXT
            )
        ''')

        self.db.execute('''
            CREATE TABLE IF NOT EXISTS series
            (
                id INTEGER PRIMARY KEY,
                name TEXT,
                alt_name TEXT
            )
        ''')

        self.db.execute('''
            CREATE TABLE IF NOT EXISTS genres
            (
                id INTEGER PRIMARY KEY,
                name TEXT,
                description TEXT
            )
        ''')

        self.db.execute('''
            CREATE TABLE IF NOT EXISTS tags
            (
                id INTEGER PRIMARY KEY,
                name TEXT,
                description TEXT
            )
        ''')

        self.db.execute('''
            CREATE TABLE IF NOT EXISTS books_artists
            (
                bookID INTEGER,
                artistID INTEGER
            )
        ''')

        self.db.execute('''
            CREATE TABLE IF NOT EXISTS books_genres
            (
                bookID INTEGER,
                genreID INTEGER
            )
        ''')

        self.db.execute('''
            CREATE TABLE IF NOT EXISTS books_tags
            (
                bookID INTEGER,
                tagID INTEGER
            )
        ''')

        self.db.execute('''
            CREATE TABLE IF NOT EXISTS characters
            (
                id INTEGER PRIMARY KEY,
                bookID INTEGER
            )
        ''')

        self.db.execute('''
            CREATE TABLE IF NOT EXISTS traits
            (
                id INTEGER PRIMARY KEY,
                name TEXT,
                description TEXT
            )
        ''')

        self.db.execute('''
            CREATE TABLE IF NOT EXISTS characters_traits
            (
                characterID INTEGER,
                traitID INTEGER
            )
        ''')

        self.conn.commit()



    def dict_factory(self, cursor, row):
        """Used by sqlite3 to return data as dicts instead of tuples
        """
        info = {}
        for idx, col in enumerate(cursor.description):
            info[col[0]] = row[idx]
        return info



    def get_metadata(self):
        """Gets a list for each non-book table

        Returns
            {str: [ListItem]}: keys are table names
        """
        data = {
            'artists': [],
            'series': [],
            'genres': [],
            'tags': [],
            'traits': []
        }

        self.db.execute('SELECT * FROM artists ORDER BY name COLLATE NOCASE')
        temp = self.db.fetchall()
        for entry in temp:
            item = ListItem(entry['id'], entry['name'], 'artists')
            data['artists'].append(item)

        self.db.execute('SELECT * FROM series ORDER BY name COLLATE NOCASE')
        temp = self.db.fetchall()
        for entry in temp:
            item = ListItem(entry['id'], entry['name'], 'series')
            data['series'].append(item)

        self.db.execute('SELECT * FROM genres ORDER BY name COLLATE NOCASE')
        temp = self.db.fetchall()
        for entry in temp:
            item = ListItem(entry['id'], entry['name'], 'genres')
            data['genres'].append(item)

        self.db.execute('SELECT * FROM tags ORDER BY name COLLATE NOCASE')
        temp = self.db.fetchall()
        for entry in temp:
            item = ListItem(entry['id'], entry['name'], 'tags')
            data['tags'].append(item)

        self.db.execute('SELECT * FROM traits ORDER BY name COLLATE NOCASE')
        temp = self.db.fetchall()
        for entry in temp:
            item = ListItem(entry['id'], entry['name'], 'traits')
            data['traits'].append(item)

        return data



    def get_books(self, filters, sort_by):
        """Gets a list of books that satisfy the search filters

        Dynamically builds a sqlite3 query string based on the information provided by filters

        Args:
            filters (dict, optional): filters to filter by from search panel
            sort_by (int): the way the books are to be sorted

        Returns:
            [dict]
        """
        sort_query = {
            const.Sort.ALPHA_ASC: 'books.name COLLATE NOCASE ASC',
            const.Sort.ALPHA_DESC: 'books.name COLLATE NOCASE DESC',
            const.Sort.RATING_ASC: 'books.rating ASC',
            const.Sort.RATING_DESC: 'books.rating DESC',
            const.Sort.PAGES_ASC: 'books.pages ASC',
            const.Sort.PAGES_DESC: 'books.pages DESC',
            const.Sort.DATE_ASC: 'books.date_added ASC',
            const.Sort.DATE_DESC: 'books.date_added DESC',
            const.Sort.RANDOM: 'random()'
        }

        if not filters: # if filters are not sent (like during startup), just give a list of all the books back
            self.db.execute('SELECT * FROM books ORDER BY ' + sort_query[sort_by])
            return self.db.fetchall()

        # shorthanding the filter keys
        and_data = filters[const.Filters.AND]
        not_data = filters[const.Filters.NOT]
        or_data = filters[const.Filters.OR]

        and_block = []
        not_block = []
        or_block = []
        count_block = []
        character_block = ''

        # AND SIMPLE
        and_block.append(f'(books.name LIKE "%{and_data["title"]}%" OR books.alt_name LIKE "%{and_data["title"]}%")') if and_data['title'] else None
        and_block.append(f'books.rating={and_data["rating"][0]}') if and_data['rating'][0] >= 0 and and_data['rating'][1] == 0 else None
        and_block.append(f'books.rating>={and_data["rating"][0]}') if and_data['rating'][0] >= 0 and and_data['rating'][1] == 2 else None
        and_block.append(f'books.rating IS NULL') if and_data['rating'][0] < 0 and and_data['rating'][1] == 0 else None
        and_block.append(f'books.pages>={and_data["pages_low"]}') if and_data['pages_low'] else None
        and_block.append(f'books.pages<={and_data["pages_high"]}') if and_data['pages_high'] else None
        and_block.append(f'books.date_added>="{and_data["date_low"]}"') if and_data['date_low'] > datetime(1900, 1, 1, 0, 0, 0, 0) else None
        and_block.append(f'books.date_added<="{and_data["date_high"]}"') if and_data['date_high'] > datetime(1900, 1, 1, 0, 0, 0, 0) else None

        # AND COMPLEX
        if and_data['artists'] == None: # different from being empty
            and_block.append('artistID IS NULL')
        elif and_data['artists']:
            and_block.append('(' + '\n\tOR '.join([f'artistID={id_}' for id_ in and_data['artists']]) + ')')

        if and_data['series'] == None: # different from being empty
            and_block.append('series IS NULL')
        elif and_data['series']:
            and_block.append('(' + '\n\tOR '.join([f'books.series={id_}' for id_ in and_data['series']]) + ')')

        if and_data['genres'] == None: # different from being empty
            and_block.append('genreID IS NULL')
        elif and_data['genres']:
            and_block.append('(' + '\n\tOR '.join([f'genreID={id_}' for id_ in and_data['genres']]) + ')')

        if and_data['tags'] == None: # different from being empty
            and_block.append('tagID IS NULL')
        elif and_data['tags']:
            and_block.append('(' + '\n\tOR '.join([f'tagID={id_}' for id_ in and_data['tags']]) + ')')

        if and_data['characters'] == None:
            # and_block.append('') TODO
            pass
        elif and_data['characters']:
            character_block += '\n\tbooks.id IN ' +  '\n\tAND books.id IN '.join([f'\n\t\t(SELECT DISTINCT bookId\n\t\tFROM characters_traits LEFT JOIN characters ON characters.id = characterID\n\t\tWHERE traitID = {" OR traitID = ".join([str(trait_id) for trait_id in character])}\n\t\tGROUP BY characterID\n\t\tHAVING COUNT(characterID) = {len(character)})' for character in and_data['characters']])

        # NOT
        not_block += [f'artistID={id_}' for id_ in not_data['artists']]
        not_block += [f'books.series={id_}' for id_ in not_data['series']]
        not_block += [f'genreID={id_}' for id_ in not_data['genres']]
        not_block += [f'tagID={id_}' for id_ in not_data['tags']]
        character_block += '\n\tAND books.id NOT IN ' if character_block else '\n\tbooks.id NOT IN '
        character_block += '\n\tAND books.id NOT IN '.join([f'\n\t\t(SELECT DISTINCT bookId\n\t\tFROM characters_traits LEFT JOIN characters ON characters.id = characterID\n\t\tWHERE traitID = {" OR traitID = ".join([str(trait_id) for trait_id in character])}\n\t\tGROUP BY characterID\n\t\tHAVING COUNT(characterID) = {len(character)})' for character in and_data['characters']])

        # OR
        or_block += [f'artistID={id_}' for id_ in or_data['artists']]
        or_block += [f'books.series={id_}' for id_ in or_data['series']]
        or_block += [f'genreID={id_}' for id_ in or_data['genres']]
        or_block += [f'tagID={id_}' for id_ in or_data['tags']]
        character_block += '\n\tOR books.id IN ' if character_block else '\n\tbooks.id IN '
        character_block += '\n\tOR books.id IN '.join([f'\n\t\t(SELECT DISTINCT bookId\n\t\tFROM characters_traits LEFT JOIN characters ON characters.id = characterID\n\t\tWHERE traitID = {" OR traitID = ".join([str(trait_id) for trait_id in character])}\n\t\tGROUP BY characterID\n\t\tHAVING COUNT(characterID) = {len(character)})' for character in and_data['characters']])

        # count
        count_block.append(f'COUNT(DISTINCT artistID)={len(and_data["artists"])}') if and_data['artists'] and len(and_data['artists']) > 1 else None
        count_block.append(f'COUNT(DISTINCT books.series)={len(and_data["series"])}') if and_data['series'] and len(and_data['series']) > 1 else None
        count_block.append(f'COUNT(DISTINCT genreID)={len(and_data["genres"])}') if and_data['genres'] and len(and_data['genres']) > 1 else None
        count_block.append(f'COUNT(DISTINCT tagID)={len(and_data["tags"])}') if and_data['tags'] and len(and_data['tags']) > 1 else None


        # check if there are even any search filters
        if not and_block and not not_block and not or_block:
            self.db.execute('SELECT * FROM books ORDER BY ' + sort_query[sort_by])
            return self.db.fetchall()


        # start building the query string
        base_query = ('SELECT DISTINCT books.* FROM books\n'
        '\tLEFT JOIN books_artists ON books_artists.bookID=books.id\n'
        '\tLEFT JOIN books_genres ON books_genres.bookID=books.id\n'
        '\tLEFT JOIN books_tags ON books_tags.bookID=books.id')

        and_string = '\nWHERE\n\t' + '\n\tAND '.join(and_block) if and_block else ''
        count_string = '\nGROUP BY books.id\nHAVING\n\t' + '\n\tAND '.join(count_block) if count_block else ''
        not_string = '\nEXCEPT\n\t' + base_query.replace('\n', '\n\t') + '\n\tWHERE\n\t\t' + '\n\t\tOR '.join(not_block) if not_block else ''
        or_string = '\n\tOR '.join(or_block)

        character_block = '\nWHERE' + character_block if not and_string else '\n\tAND ' + character_block
        query = base_query + and_string + character_block + count_string + not_string
        query = ('SELECT DISTINCT books.* FROM books\n'
        '\tINNER JOIN\n\t\t(' + query.replace("\n", "\n\t\t") + ') AS temp ON temp.id=books.id\n'
        '\tLEFT JOIN books_artists ON books_artists.bookID=books.id\n'
        '\tLEFT JOIN books_genres ON books_genres.bookID=books.id\n'
        '\tLEFT JOIN books_tags ON books_tags.bookID=books.id\n'
        'WHERE\n\t' + or_string) if or_block else query
        query = query + '\nORDER BY ' + sort_query[sort_by]

        self.db.execute(query)
        return self.db.fetchall()



    def get_book(self, book_id: int):
        """Gets all the data in table book. should be used for just getting basic info. for all info use get_book_info()

        Args:
            book_id (int)
        """
        self.db.execute(f'SELECT * FROM books WHERE books.id={book_id}')
        return self.db.fetchone()



    def get_series_for(self, book_id: int):
        self.db.execute(f'SELECT connections.id, connections.name, connections.series_order, connections.directory FROM books selected JOIN books connections ON selected.series = connections.series WHERE selected.id = {book_id} ORDER BY connections.series_order ASC')
        return self.db.fetchall()



    def get_book_info(self, book_id: int):
        """Returns all relevant information about a book.

        Used mainly to populate info panel.

        Note:
            For series, artists, genres, and tags fields, returns the ID instead of the str name

        Args:
            book_id (int)

        Returns:
            dict
        """
        self.db.execute('SELECT * FROM books WHERE books.id=?', (book_id,))
        info = self.db.fetchone()

        self.db.execute('SELECT series.id, series.name FROM series INNER JOIN books ON series.id=books.series WHERE books.id=?', (book_id,))
        series = self.db.fetchone()
        info['series'] = (ListItem(-1, '', 'series') if not series else ListItem(series['id'], series['name'], 'series'))

        self.db.execute('SELECT artists.id, artists.name FROM artists INNER JOIN books_artists ON artistID=artists.id INNER JOIN books ON bookID=books.id WHERE bookID=?', (book_id,))
        artists = self.db.fetchall()
        info['artists'] = []
        for a in artists:
            info['artists'].append(ListItem(a['id'], a['name'], 'artists'))

        self.db.execute('SELECT genres.id, genres.name FROM genres INNER JOIN books_genres ON genreID=genres.id INNER JOIN books ON bookID=books.id WHERE bookID=?', (book_id,))
        genres = self.db.fetchall()
        info['genres'] = []
        for g in genres:
            info['genres'].append(ListItem(g['id'], g['name'], 'genres'))

        self.db.execute('SELECT tags.id, tags.name FROM tags INNER JOIN books_tags ON tagID=tags.id INNER JOIN books ON bookID=books.id WHERE bookID=?', (book_id,))
        tags = self.db.fetchall()
        info['tags'] = []
        for t in tags:
            info['tags'].append(ListItem(t['id'], t['name'], 'tags'))

        self.db.execute('SELECT characterID, traits.id, name FROM traits INNER JOIN characters_traits ON traits.id = traitID INNER JOIN characters ON characters.id = characterID WHERE bookID = ?', (book_id,))
        characters = self.db.fetchall()
        info['characters'] = dict()
        for c in characters:
            if c['characterID'] not in info['characters']:
                info['characters'][c['characterID']] = []
            info['characters'][c['characterID']].append(ListItem(c['id'], c['name'], 'traits'))

        return info



    def create_metadata(self, table: str, name: str):
        """Creates entries with the given information into the given table

        Note:
            Should only be used for non-book tables!

        Args:
            table (str)
            name (str)

        Raises:
            exceptions.DuplicateEntry: If the entry that's attempting to be created already exists in the database
        """
        self.db.execute(f'SELECT * FROM {table} WHERE name LIKE "{name}"')
        if self.db.fetchone():
            raise exceptions.DuplicateEntry

        self.db.execute(f'INSERT INTO {table}(name) VALUES("{name}")')
        self.conn.commit()



    def delete_metadata(self, table: str, id_: int):
        """Deletes an entry and all references to that entry from all tables

        Args:
            table (str)
            id_ (int)
        """
        if table == 'books':
            # deletes the book entry and all entries related to it in books_artists, books_genres, books_tags
            self.db.execute('DELETE FROM books_artists WHERE bookID=?', (id_,))
            self.db.execute('DELETE FROM books_genres WHERE bookID=?', (id_,))
            self.db.execute('DELETE FROM books_tags WHERE bookID=?', (id_,))
            self.db.execute('DELETE FROM books WHERE id=?', (id_,))
        elif table == 'series':
            # deletes the series entry and sets any book's series field to NULL
            self.db.execute('UPDATE books SET series=NULL WHERE series=?', (id_,))
            self.db.execute('DELETE FROM series WHERE id=?', (id_,))
        elif table in ['artists', 'genres', 'tags']:
            # deletes the entry and all entries related to it in its respective many-to-many through table
            self.db.execute(f'DELETE FROM books_{table} WHERE {table[:-1]}ID={id_}')
            self.db.execute(f'DELETE FROM {table} WHERE id={id_}')
        elif table == 'traits':
            # deletes the entry and removes the trait from all characters and deletes any characters that don't have any traits
            self.db.execute(f'DELETE FROM characters_traits WHERE traitID={id_}')
            self.db.execute('DELETE FROM characters WHERE id NOT IN (SELECT characterID FROM characters_traits)')
            self.db.execute(f'DELETE FROM traits WHERE id={id_}')

        self.conn.commit()



    def rename_metadata(self, table: str, id_: int, new_name: str):
        """Renames a metadata entry

        Args:
            table (str)
            id_ (int)
            new_name (str)
        """
        self.db.execute(f'UPDATE {table} SET name="{new_name}" WHERE id={id_}')
        self.conn.commit()



    def add_character(self, book_id: int, traits: list[int]) -> int:
        pass



    def remove_character(self, character_id: int):
        # also needs to delete characters properly, delete from characters where bookID is null
        pass



    def add_book(self, name, directory, alt_name='NULL', series='NULL', series_order='NULL', pages='NULL', rating='NULL', notes='NULL', zoom=1, bookmark=0):
        """Creates a new book entry
        """
        if alt_name != 'NULL':
            alt_name = f'"{alt_name}"'
        if notes != 'NULL':
            notes = f'"{notes}"'
        self.db.execute(f'INSERT INTO books(name, alt_name, series, series_order, pages, rating, notes, directory, zoom, bookmark) VALUES("{name}", {alt_name}, {series}, {series_order}, {pages}, {rating}, {notes}, "{directory}", {zoom}, {bookmark})')
        self.conn.commit()



    def update_book(self, data: dict):
        """Updates a book's data

        This basically cleans the book's DB entry and rebuilds it with the specific info.
        Instead of editing only the parts we changed, we re-write the whole DB entry.

        Args:
            data (dict)
        """
        self.db.execute('UPDATE books SET name=?, alt_name=?, series=?, series_order=?, rating=?, notes=? WHERE id=?', (data['title'], data['alt_title'], data['series'], data['series_order'], data['rating'], data['notes'], data['id']))

        self.db.execute('DELETE FROM books_artists WHERE bookID=?', (data['id'],))
        for artist in data['artists']:
            self.db.execute('INSERT INTO books_artists VALUES(?, ?)', (data['id'], artist))

        self.db.execute('DELETE FROM books_genres WHERE bookID=?', (data['id'],))
        for genre in data['genres']:
            self.db.execute('INSERT INTO books_genres VALUES(?, ?)', (data['id'], genre))

        self.db.execute('DELETE FROM books_tags WHERE bookID=?', (data['id'],))
        for tag in data['tags']:
            self.db.execute('INSERT INTO books_tags VALUES(?, ?)', (data['id'], tag))

        self.db.execute(f'DELETE FROM characters_traits WHERE characterID IN (SELECT id FROM characters WHERE bookID = {data["id"]})')
        self.db.execute(f'DELETE FROM characters WHERE bookID = {data["id"]}')
        for character in data['characters']:
            if not character: # don't add characters without traits
                continue
            self.db.execute(f'INSERT INTO characters(bookID) VALUES({data["id"]}) RETURNING *')
            added_data = self.db.fetchone()
            for trait in character:
                self.db.execute(f'INSERT INTO characters_traits VALUES({added_data["id"]}, {trait})')

        self.conn.commit()



    def delete_book(self, id_: int):
        """Deletes a book from the DB and all references to it

        Args:
            id_ (int)
        """
        self.db.execute(f'DELETE FROM books WHERE id={id_}')
        self.db.execute(f'DELETE FROM books_artists WHERE bookID={id_}')
        self.db.execute(f'DELETE FROM books_genres WHERE bookID={id_}')
        self.db.execute(f'DELETE FROM books_tags WHERE bookID={id_}')
        self.db.execute(f'DELETE FROM characters_traits WHERE characterID IN (SELECT id FROM characters WHERE bookID={id_})')
        self.db.execute(f'DELETE FROM charaters WHERE bookID={id_}')
        self.conn.commit()



    def get_book_directories(self):
        """Used to get a list of all the directories for books in the database

        Only really used for Home.scan_directory()

        Returns:
            [str]
        """
        self.db.execute('SELECT directory FROM books')
        return [x['directory'] for x in self.db.fetchall()]



    def set_book_zoom(self, id_: int, zoom: float):
        self.db.execute(f'UPDATE books SET zoom = {zoom} WHERE id = {id_}')
        self.conn.commit()



    def set_bookmark(self, id_: int, page: int):
        self.db.execute(f'UPDATE books SET bookmark = {page} WHERE id = {id_}')
        self.conn.commit()