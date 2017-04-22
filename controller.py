from flask import Flask, render_template, request, send_from_directory
from werkzeug import secure_filename
import uuid
import os
import config
from utils import generate_partial_uuid, generate_search_friendly_name 
from models.books import insert_new_book_to_motherlode, is_book_invalid, is_author_invalid, is_isbn_invalid, is_cover_invalid, create_image_path_for_db, Book

app = Flask(__name__)

@app.route('/', methods=['GET'])
def render_index():
    return("Hi", 200)


@app.route('/motherlode/add', methods=['GET'])
def render_add_book_form():
    return render_template('add_books.html', title="Add Books")


@app.route('/motherlode/add', methods=['POST'])
def add_book():

    if 'book-title' not in request.form or is_book_invalid(request.form['book-title']):
        return "Book should have a name"

    if 'author' not in request.form or is_author_invalid(request.form['author']):
        return "Please specify the author's name"

    if 'isbn' not in request.form or is_isbn_invalid(request.form['isbn']):
        return "Please mention the book's ISBN"

    # Book cover
    if 'book-image' not in request.files or request.files['book-image'].filename == '':
        image_path_in_db = 'default-image.jpeg'

    elif is_cover_invalid(request.files['book-image'], request.files['book-image'].filename):
        return "Improper image. Please follow conventions"

    else:
        image_path_in_db = create_image_path_for_db(request.files['book-image'].filename)
        book_cover_file = request.files['book-image']
        # save file to FS
        book_cover_file.save(os.path.join('static', 'book_covers', image_path_in_db))
        
    book_to_save = Book(request.form['book-title'],
                        request.form['author'],
                        request.form['isbn'],
                        image_path_in_db,
                        generate_search_friendly_name(request.form['book-title']))

    insert_new_book_to_motherlode(book_to_save)

    return "success"
    

@app.route('/sign_in', methods=['GET'])
def render_sign_in_form():
    return render_template('sign_in.html', title="Sign In")

@app.route('/sign_in', methods=['POST'])
def sign_in():
    return ("hi", 200)

@app.route('/sign_up', methods=['GET'])
def render_sign_up_form():
    return render_template('sign_up.html', title="Sign Up")

@app.route('/sign_up', methods=['POST'])
def sign_up():
    return ("hi", 200)