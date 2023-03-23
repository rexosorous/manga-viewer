# standard libraries
from datetime import datetime
from string import Template
import sqlite3

# dependencies
from PyQt5.QtWidgets import QListWidgetItem

# local modules
import constants as const
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



    def get_books(self, filters=None, sort_by = const.Sort.ALPHA_ASC):
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

        if filters == None: # if filters are not sent (like during startup), just give a list of all the books back
            self.db.execute('SELECT * FROM books ORDER BY ' + sort_query[sort_by])
            return self.db.fetchall()

        # basic fields
        basic_subquery = 'SELECT id FROM books'
        where_clauses = []
        if title := filters['basic']['title']:
            where_clauses.append(f"(name LIKE '%{title}%' OR alt_name LIKE '%{title}%')")
        if (rating := filters['basic']['rating'][0]) >= 0:
            operator = '>=' if filters['basic']['rating'][1] else '='
            where_clauses.append(f'rating {operator} {rating}')
        if filters['basic']['rating'][0] < 0 and filters['basic']['rating'][1] == 0:
            where_clauses.append(f'rating IS NULL')
        if pages_low := filters['basic']['pages_low']:
            where_clauses.append(f'pages >= {pages_low}')
        if pages_high := filters['basic']['pages_high']:
            where_clauses.append(f'pages <= {pages_high}')
        if (date_low := filters['basic']['date_low']) > datetime(1900, 1, 1, 0, 0, 0, 0):
            where_clauses.append(f"date_added >= '{date_low}'")
        if (date_high := filters['basic']['date_high']) > datetime(1900, 1, 1, 0, 0, 0, 0):
            where_clauses.append(f"date_added <= '{date_high}'")
        # combine where clauses and add it to query
        where_statement = '\n\tAND '.join(where_clauses)
        if where_statement:
            basic_subquery += '\nWHERE ' + where_statement

        self.db.execute(basic_subquery)
        results = self.db.fetchall()
        prev_results = [x['id'] for x in results]

        # all many to many fields except for characters (artists, genres, and tags)
        with open('queries/mtm_fields_subquery.sql', 'r') as file:
            mtm_fields_subquery = file.read()

        for field in ['artists', 'genres', 'tags']:
            if field in filters:
                query_vars = {
                    'linking_table': f'books_{field}',
                    'field': f'{field[:-1]}ID',
                    'null_search': False,
                    'has_and': filters[field].has(const.Filters.AND),
                    'and_list': filters[field].get_query_list(const.Filters.AND),
                    'and_list_length': len(filters[field].data[const.Filters.AND]),
                    'has_or': filters[field].has(const.Filters.OR),
                    'or_list': filters[field].get_query_list(const.Filters.OR),
                    'has_not': filters[field].has(const.Filters.NOT),
                    'not_list': filters[field].get_query_list(const.Filters.NOT),
                    'has_prev_results': prev_results != None,
                    'prev_results_list': f'({",".join(map(str, prev_results))})' if prev_results != None else '()'
                }
            else: # null search
                query_vars = {
                    'linking_table': f'books_{field}',
                    'field': f'{field[:-1]}ID',
                    'null_search': True,
                    'has_and': False,
                    'and_list_length': 0,
                    'and_list': (),
                    'has_or': False,
                    'or_list': (),
                    'has_not': False,
                    'not_list': (),
                    'has_prev_results': prev_results != None,
                    'prev_results_list': f'({",".join(map(str, prev_results))})' if prev_results != None else ()
                }

            query = Template(mtm_fields_subquery).safe_substitute(query_vars)
            self.db.execute(query)
            results = self.db.fetchall()
            prev_results = [x['id'] for x in results]
            if len(prev_results) == 0:
                break

        # characters are special because of the way they have to link the tables
        with open('queries/characters_subquery.sql', 'r') as file:
            characters_subquery = file.read()

        if 'characters' in filters:
            for character in filters['characters']:
                query_vars = {
                    'null_search': False,
                    'has_and': character.has(const.Filters.AND),
                    'and_list': character.get_query_list(const.Filters.AND),
                    'and_list_length': len(character.data[const.Filters.AND]),
                    'has_or': character.has(const.Filters.OR),
                    'or_list': character.get_query_list(const.Filters.OR),
                    'has_not': character.has(const.Filters.NOT),
                    'not_list': character.get_query_list(const.Filters.NOT),
                    'has_prev_results': prev_results != None,
                    'prev_results_list': f'({",".join(map(str, prev_results))})' if prev_results != None else ()
                }

                query = Template(characters_subquery).safe_substitute(query_vars)
                self.db.execute(query)
                results = self.db.fetchall()
                prev_results = [x['id'] for x in results]
        else:
            query_vars = {
                'null_search': True,
                'has_and': False,
                'and_list': (),
                'and_list_length': 0,
                'has_or': False,
                'or_list': (),
                'has_not': False,
                'not_list': (),
                'has_prev_results': prev_results != None,
                'prev_results_list': f'({",".join(map(str, prev_results))})' if prev_results != None else ()
            }

            query = Template(characters_subquery).safe_substitute(query_vars)
            self.db.execute(query)
            results = self.db.fetchall()
            prev_results = [x['id'] for x in results]


        self.db.execute(f'SELECT * FROM books WHERE id IN ({",".join(map(str, prev_results))}) ORDER BY {sort_query[sort_by]}')
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
        self.db.execute(f'DELETE FROM characters WHERE bookID={id_}')
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