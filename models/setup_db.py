import sqlite3
import os
from config import path_to_db 
from utils import connect_to_sqlite_db, close_sqlite_connection


def setup():
    connection, cursor = connect_to_sqlite_db(path_to_db)

    # Setup books table
    # To make it easy to search similar books via ISBN, it's 
    # better to set ISBN to character
    # image_file contains a part of the book's name + 5 characters of an UUID
    # It's done to avoid clashes in case 2 books have the same title
    create_books = (
        'CREATE TABLE books ('
        'isbn CHARACTER(13) PRIMARY KEY,'
        'name VARCHAR(100) NOT NULL,'
        'search_name VARCHAR(100) NOT NULL,'
        'author VARCHAR(50) NOT NULL,'
        'image_path CHARACTER(50)'
        ');'
    )
    cursor.execute(create_books)


    # Setup users table
    # autoincrement uses extra cpu but doing it nevertheless given the scale
    create_users = (
        'CREATE TABLE users ('
        'id INTEGER PRIMARY KEY,' # this autoincrements by itself
        'username CHARACTER(15) NOT NULL,'
        'password_hash TEXT NOT NULL,'
        'full_name VARCHAR(50) NOT NULL'
        ');'
    )
    cursor.execute(create_users)

    # Setup user favourite book tables
    create_favourite_books = (
        'CREATE TABLE favourite ('
        'user_id INTEGER NOT NULL,'
        'isbn CHARACTER(13) NOT NULL,'
        'FOREIGN KEY(isbn) REFERENCES books(isbn)'
        ');'
    )
    cursor.execute(create_favourite_books)

    # Setup book vote tables
    # -1 for downvote, +1 for upvote
    create_votes = (
        'CREATE TABLE votes ('
        'user_id INTEGER NOT NULL,'
        'isbn CHARACTER(13) NOT NULL,'
        'vote INTEGER NOT NULL'
        ');'
    )
    cursor.execute(create_votes)

    close_sqlite_connection(connection)