import sqlite3
from utils import connect_to_sqlite_db, close_sqlite_connection
from config import path_to_db, books_per_page
from models.books import does_isbn_exist, get_details_using_isbn
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
    connection, cursor = connect_to_sqlite_db(path_to_db)
    
    # is_user_book_unique checks if there are copies of the same id and isbn
    # bad naming convention. Fix late
    if does_isbn_exist(isbn) and does_user_id_exist(id) and not is_user_book_unique(id, isbn):
        cursor.execute("DELETE FROM favourite WHERE user_id = ? AND isbn = ?", (id, isbn))
        result = True
    else:
        result = False
    
    close_sqlite_connection(connection)
    return result

def handle_pagination(user_id, page, total_books):
    connection, cursor = connect_to_sqlite_db(path_to_db)
    result = {'prev': None, 'next': None, 'books': [], "current": page}
    if total_books:
        if total_books > (page * books_per_page):
            result['next'] = True 
        if page > 1:
            result['prev'] = True
        
        # Getting the relevant stuff from DB
        cursor.execute("SELECT isbn FROM favourite WHERE user_id = ? LIMIT ? OFFSET ?",
                        (user_id, books_per_page, (page - 1) * books_per_page))
        
        for individual_isbn in cursor.fetchall():
            isbn, title, author, image = get_details_using_isbn(individual_isbn[0])
            result['books'].append({'isbn': isbn,
                                    'title': title,
                                    'author': author,
                                    'image': image})

    close_sqlite_connection(connection)
    return result