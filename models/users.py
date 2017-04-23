from config import path_to_db
import hashlib
from utils import connect_to_sqlite_db, close_sqlite_connection
import re

class User:
    def __init__(self, full_name, username, password):
        self.username = username
        self.password_hash = hashlib.md5(password).hexdigest()
        self.full_name = full_name
        self.id = "NULL" # useful for autoincrementing

def create_new_user(user_ob):
    connection, cursor = connect_to_sqlite_db(path_to_db)
    cursor.execute(
        "INSERT INTO users (username, password_hash, full_name) VALUES (?, ?, ?)",
        (user_ob.username, user_ob.password_hash, user_ob.full_name))
    close_sqlite_connection(connection)


def validate_and_get_details(username, password):
    connection, cursor = connect_to_sqlite_db(path_to_db)

    # Check if the username exists
    cursor.execute("SELECT (SELECT count() FROM users where username = ?) as count", (username,))
    if cursor.fetchone()[0] == 0:
        close_sqlite_connection(connection)
        return (False, None, None)

    cursor.execute("SELECT password_hash, id, full_name FROM users where username = ?", (username, ))
    password_hash, user_id, full_name = cursor.fetchone()

    if password_hash != hashlib.md5(password).hexdigest():
        close_sqlite_connection(connection)
        return (False, None, None)
    else:
        close_sqlite_connection(connection)
        return (True, user_id, full_name)


def is_full_name_invalid(full_name):
    # same like author
    validate = re.compile(r'[^a-zA-Z\.\' ]').search
    if (len(full_name) > 50):
        return True
    
    if len(full_name.replace(" ", '').replace('\t', '')) < 1:
        return True

    if (validate(full_name)):
        return True

    return False

def is_username_invalid(username):
    validate = re.compile(r'[^a-z0-9]').search
    if (len(username) > 15):
        return True
    
    if (validate(username)):
        return True

    return False

def does_user_id_exist(id):
    connection, cursor = connect_to_sqlite_db(path_to_db)
    result = None
    cursor.execute("SELECT (SELECT count() FROM users WHERE id = ?) as count", (id, ))
    if cursor.fetchone()[0] > 0:
        result = True
    else:
        result = False

    close_sqlite_connection(connection)
    return result
    

def username_already_exists(username):
    connection, cursor = connect_to_sqlite_db(path_to_db)
    cursor.execute("SELECT (SELECT count() FROM users WHERE username = ?) as count", (username,))
    if cursor.fetchone()[0] > 0:
        close_sqlite_connection(connection)
        return True

    close_sqlite_connection(connection)
    return False

def get_full_name_from_id(id):
    connection, cursor = connect_to_sqlite_db(path_to_db)
    cursor.execute("SELECT full_name FROM users WHERE id = ?", (id, ))
    name = cursor.fetchone()[0]
    close_sqlite_connection(connection)
    return name

def is_password_weak(password):
    numeric = re.compile(r'[0-9]').search
    special = re.compile(r'[!@#\$\^\*\.]').search
    upper_case = re.compile(r'[A-Z]').search

    if len(password) < 6:
        return True

    if not numeric(password):
        return True
    
    if not special(password):
        return True

    if not upper_case(password):
        return True

    return False