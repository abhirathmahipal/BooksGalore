from werkzeug import secure_filename
import os
from utils import generate_search_friendly_name, generate_partial_uuid, connect_to_sqlite_db, close_sqlite_connection
from config import path_to_db, books_per_page
import re
import imghdr


class Book:
    'Class to make sense of books'
    # add getters and setter and sanity checks here if time permits
    def __init__(self, name, author, isbn, image_path, search_name):
        self.name = name
        self.author = author
        self.isbn = isbn.replace("-", '')
        self.image_path = image_path
        self.search_name = search_name


def insert_new_book_to_motherlode(book_ob):
    connection, cursor = connect_to_sqlite_db(path_to_db)
    cursor.execute(
        "INSERT INTO books (isbn, name, search_name, author, image_path) VALUES(?, ?, ?, ?, ?)",
        (book_ob.isbn, book_ob.name, book_ob.search_name, book_ob.author, book_ob.image_path))
    close_sqlite_connection(connection)

def is_book_invalid(book_title):
    validate = re.compile(r'[^0-9a-zA-Z \']').search

    if (len(book_title) > 100):
        return True

    if (len(book_title.replace(' ', '').replace('\t', '')) < 1):
        return True

    if (validate(book_title)):
        return True

    return False


def is_author_invalid(author):
    #only allowing a-z, . ' and spaces
    validate = re.compile(r'[^a-zA-Z\.\' ]').search
    if (len(author) > 50):
        return True

    # if it contains less than one non space character
    if (len(author.replace(" ", '').replace('\t', '')) < 1):
        return True

    if (validate(author)):
        return True

    return False


def is_isbn_invalid(isbn):
    #only allow numbers and hypens
    validate = re.compile(r'[^0-9-]').search

    if (validate(isbn)):
        return True

    if (len(isbn.replace("-", "")) != 13):
        return True

    return False


def is_cover_invalid(uploaded_filename):
    file_name, file_extension = os.path.splitext(uploaded_filename)
    
    # extension checking
    if file_extension not in (".png", ".jpg", ".jpeg"):
        return True

    # Checking if the file actually is an image and not just any renamed file
    # if the stream if fed into imghdr, the fileobject is destroyed.
    # create a temporary file and deal with this later
    return False


def create_image_path_for_db(uploaded_filename):
    file_name, file_extension = os.path.splitext(uploaded_filename)
    secure_base_name = secure_filename(file_name)
    if len(secure_base_name) <= 40:
       return secure_base_name + generate_partial_uuid(5) + file_extension
    else:
       return secure_base_name[:40] + generate_partial_uuid(5) + file_extension

def does_isbn_exist(isbn):
    connection, cursor = connect_to_sqlite_db(path_to_db)
    cursor.execute("SELECT (SELECT count() FROM books where isbn = ?) as count", (isbn.replace("-", ''),))

    if cursor.fetchone()[0] == 1:
        result = True
    else:
        result = False

    close_sqlite_connection(connection)
    return result

def get_details_using_isbn(isbn):
    if (does_isbn_exist(isbn)):
        connection, cursor = connect_to_sqlite_db(path_to_db)
        cursor.execute("SELECT isbn, name, author, image_path FROM books where isbn = ?", (isbn, ))
        return cursor.fetchone()
    else:
        return ("Invalid", "Does Not Exist", "Invalid", 'default-image.jpeg')

def match_books_by_string(name_string):
    connection, cursor = connect_to_sqlite_db(path_to_db)
    search_param = '%' + generate_search_friendly_name(name_string) + '%'
    cursor.execute("SELECT isbn, name, author, image_path FROM books WHERE search_name like ?", (search_param, ))
    results = cursor.fetchall()
    json_results = [{'isbn': i[0], 'title': i[1], 'author': i[2], 'image': i[3]} for i in results]
    close_sqlite_connection(connection)
    return json_results