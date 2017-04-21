import sqlite3
import uuid


def connect_to_sqlite_db(file_path):
    connection = sqlite3.connect(file_path)
    cursor = connection.cursor()
    return (connection, cursor)


def close_sqlite_connection(connection):
    connection.commit()
    connection.close()


def generate_partial_uuid(length):
    return str(uuid.uuid4())[:length]

