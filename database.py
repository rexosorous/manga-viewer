import sqlite3



class DBHandler:
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



    def get_books(self):
        """Gets a list of every book in the dictionary

        Returns:
            list of dicts
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