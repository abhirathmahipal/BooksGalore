import uuid
import sqlite3


def connect_to_sqlite_db(file_path):
    connection = sqlite3.connect(file_path)
    cursor = connection.cursor()
    return (connection, cursor)


def close_sqlite_connection(connection):
    connection.commit()
    connection.close()


def generate_partial_uuid(length):
    return str(uuid.uuid4())[:length]


def generate_search_friendly_name(messy_string):
    return "".join(i for i in messy_string if i.isalnum()) 