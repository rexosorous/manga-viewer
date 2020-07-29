# standard libraries
import sqlite3

# dependencies
from PyQt5.QtWidgets import QListWidgetItem

# local modules
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
        self.setText(name)



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
                id INTEGER,
                name TEXT,
                alt_name TEXT,
                series INTEGER,
                series_order REAL,
                pages INTEGER,
                rating INTEGER,
                notes TEXT,
                date_added REAL, -- datetime.datetime.now().timestamp()
                directory TEXT
            )
        ''')

        self.db.execute('''
            CREATE TABLE IF NOT EXISTS artists
            (
                id INTEGER,
                name TEXT,
                alt_name TEXT
            )
        ''')

        self.db.execute('''
            CREATE TABLE IF NOT EXISTS series
            (
                id INTEGER,
                name TEXT,
                alt_name TEXT
            )
        ''')

        self.db.execute('''
            CREATE TABLE IF NOT EXISTS genres
            (
                id INTEGER,
                name TEXT,
                description TEXT
            )
        ''')

        self.db.execute('''
            CREATE TABLE IF NOT EXISTS tags
            (
                id INTEGER,
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
            'tags': []
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

        return data



    def get_books(self):
        """Gets a list of every book in the dictionary

        Returns:
            [dict]
        """
        self.db.execute('SELECT id, name, directory FROM books')
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

        self.db.execute('SELECT series.name FROM series INNER JOIN books ON series.id=books.series WHERE books.id=?', (book_id,))
        series = self.db.fetchone()
        # info['series'] = ('' if not series else series['name'])

        self.db.execute('SELECT artists.id FROM artists INNER JOIN books_artists ON artistID=artists.id INNER JOIN books ON bookID=books.id WHERE bookID=?', (book_id,))
        artists = self.db.fetchall()

        self.db.execute('SELECT genres.id FROM genres INNER JOIN books_genres ON genreID=genres.id INNER JOIN books ON bookID=books.id WHERE bookID=?', (book_id,))
        genres = self.db.fetchall()

        self.db.execute('SELECT tags.id FROM tags INNER JOIN books_tags ON tagID=tags.id INNER JOIN books ON bookID=books.id WHERE bookID=?', (book_id,))
        tags = self.db.fetchall()

        info['artists'] = [x['id'] for x in artists]
        info['genres'] = [x['id'] for x in genres]
        info['tags'] = [x['id'] for x in tags]

        return info



    def create_entry(self, table: str, name: str):
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

        self.db.execute(f'SELECT id FROM {table} ORDER BY id DESC LIMIT 1')
        last_id = self.db.fetchone()
        self.db.execute(f'INSERT INTO {table} VALUES({last_id["id"]+1}, "{name}", "")')
        self.conn.commit()



    def delete_entry(self, table: str, id_: int):
        """Deletes an entry and all references to that entry from all tables

        Args:
            table (str)
            id_ (int)
        """
        if table == 'books':
            # deletes the book entry and all entries related to it in books_artists, books_genres, books_tags
            self.db.exceute('DELETE FROM books_artists WHERE bookID=?', (id_,))
            self.db.execute('DELETE FROM books_genres WHERE bookID=?', (id_,))
            self.db.execute('DELETE FROM books_tags WHERE bookID=?', (id_,))
            self.db.execute('DELETE FROM books WHERE id=?', (id_,))
        elif table == 'series':
            # deletes the series entry and sets any book's series field to NULL
            self.db.execute('UPDATE books SET series=NULL WHERE series=?', (id_,))
            self.db.execute('DELETE FROM series WHERE id=?', (id_,))
        elif table in ['genres', 'series', 'tags']:
            # deletes the entry and all entries related to it in its respective many-to-many through table
            self.db.execute(f'DELETE FROM books_{table} WHERE {table[:-1]}ID={id_}')
            self.db.execute(f'DELETE FROM {table} WHERE id={id_}')

        self.conn.commit()