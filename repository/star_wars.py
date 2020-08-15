import logging
import sqlite3


class RepositoryError(Exception):
    pass


class StarWarsRepository:
    def __init__(self, db):
        self._db = db
        self.initialize_db()

    def initialize_db(self):
        films_table = '''
            CREATE TABLE IF NOT EXISTS films (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                release_date TEXT NOT NULL
            )
        '''
        characters_table = '''
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        '''
        file_characters_table = '''
            CREATE TABLE IF NOT EXISTS film_characters (
                film_id INTEGER,
                character_id INTEGER
            )
        '''
        try:
            connection = sqlite3.connect(self._db)
            tables = [films_table, characters_table, file_characters_table]
            [connection.execute(table) for table in tables]
        except Exception as e:
            logging.fatal(f'Couldn\'t initialize database {e}')

    def purge_db(self):
        films_table = '''
            DELETE FROM films
        '''
        characters_table = '''
            DELETE FROM characters
        '''
        file_characters_table = '''
            DELETE FROM film_characters
        '''
        try:
            connection = sqlite3.connect(self._db)
            cursor = connection.cursor()
            tables = [films_table, characters_table, file_characters_table]
            for table in tables:
                cursor.execute(table)
            connection.commit()
            connection.close()
        except Exception as e:
            logging.fatal(f'Couldn\'t initialize database {e}')

    def update_films(self, results):
        try:
            conn = sqlite3.connect(self._db)
            c = conn.cursor()
            film_id = 1
            for movie in results:
                query = f'''
                    INSERT INTO films VALUES({film_id},
                    '{movie['title']}',
                    '{movie['release_date']}')
                '''
                film_id = film_id + 1
                c.execute(query)
            conn.commit()
            conn.close()
        except Exception as e:
            logging.error(f'Repository exception {e}')
            raise RepositoryError()

    def update_actors(self, results):
        try:
            conn = sqlite3.connect(self._db)
            c = conn.cursor()
            actor_id = 1
            for actor in results:
                query = f'''
                    INSERT INTO characters VALUES({actor_id},
                    '{actor['name']}')
                '''
                c.execute(query)
                for film in actor['films']:
                    film_id = int(film.split("/")[-2])
                    query = f'''
                        INSERT INTO film_characters
                        VALUES({film_id}, {actor_id})
                    '''
                    c.execute(query)
                actor_id = actor_id + 1
            conn.commit()
            conn.close()
        except Exception as e:
            logging.error(f'Repository exception {e}')
            raise RepositoryError()

    def get_films(self):
        try:
            conn = sqlite3.connect(self._db)
            c = conn.cursor()
            query = f'''
                SELECT * FROM films
            '''
            c.execute(query)
            rows = c.fetchall()
            return rows
        except Exception as e:
            logging.error(f'Repository exception {e}')
            raise RepositoryError()

    def get_characters(self, film_id: int):
        try:
            conn = sqlite3.connect(self._db)
            c = conn.cursor()
            query = f'''
                SELECT character_id FROM film_characters
                WHERE film_id={film_id}
            '''
            c.execute(query)
            characters = c.fetchall()
            characters = [y[0] for y in characters]
            characters = ','.join(str(y) for y in characters)
            query = f'''
                SELECT * FROM characters WHERE
                id IN ({characters})
            '''
            c.execute(query)
            result = c.fetchall()
            return result
        except Exception as e:
            logging.error(f'Repository exception: {e}')
            raise RepositoryError()
