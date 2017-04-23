import sqlite3
from utils import connect_to_sqlite_db, close_sqlite_connection
from config import path_to_db
from models.books import does_isbn_exist
from models.users import does_user_id_exist


def is_user_book_unique(id, isbn):
    connection, cursor = connect_to_sqlite_db(path_to_db)

    cursor.execute("SELECT (SELECT count() FROM favourite WHERE user_id = ? AND isbn = ?) AS count", (id, isbn))
    if cursor.fetchone()[0] > 0:
        result = False
    else:
        result = True

    close_sqlite_connection(connection)

    return result

def insert_new_user_book(id, isbn):
    connection, cursor = connect_to_sqlite_db(path_to_db)
    isbn = isbn.replace("-", '')

    if does_isbn_exist(isbn) and does_user_id_exist(id) and is_user_book_unique(id, isbn):
        cursor.execute("INSERT INTO favourite (user_id, isbn) VALUES (?, ?)", (id, isbn))
        result = True
    else:
        result = False

    close_sqlite_connection(connection)
    return result


def total_fav_books(id):
    connection, cursor = connect_to_sqlite_db(path_to_db)
    
    cursor.execute("SELECT (SELECT count() FROM favourite WHERE user_id = ?) AS count", (id, ))
    count = cursor.fetchone()[0]
    close_sqlite_connection(connection)
    return count

def delete_user_book(id, isbn):
    return True