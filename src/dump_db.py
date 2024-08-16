import sqlite3

from config import path_db
from src.parser import parse


def create_db():
    """ Создание таблицы. """
    sql_create = """
    CREATE TABLE IF NOT EXISTS capitalize (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        country TEXT,
        city TEXT,
        area TEXT,
        people TEXT,
        official_language TEXT,
        valuta TEXT,
        phone_code TEXT,
        countries_url TEXT,
        image TEXT
    )
     """

    try:
        with sqlite3.connect(path_db) as conn:
            cursor = conn.cursor()
            cursor.execute('DROP TABLE IF EXISTS capitalize')
            cursor.execute(sql_create)
            conn.commit()
    except sqlite3.Error as e:
        print(e)


def dump_db():
    """ Загрузка БД. """
    info = parse()
    try:
        with sqlite3.connect(path_db) as conn:
            cur = conn.cursor()

            cur.executemany(
                "INSERT INTO capitalize (country, city, area, people, official_language, valuta, phone_code, countries_url, image) VALUES(?,?,?,?,?,?,?,?,?)",
                info)
            cur.close()
            conn.commit()
        print(f"БД сформирована!")
    except sqlite3.Error as e:
        print(e)


if __name__ == '__main__':
    pass
