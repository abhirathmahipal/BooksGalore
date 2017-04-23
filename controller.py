import os
import uuid
import config
from flask import Flask, render_template, request, send_from_directory, url_for, redirect, jsonify
from flask.ext.login import (LoginManager, UserMixin, login_required,
                             login_user, logout_user, current_user)
from models.books import (Book, create_image_path_for_db,
                          insert_new_book_to_motherlode, is_author_invalid,
                          is_book_invalid, is_cover_invalid, is_isbn_invalid,
                          get_details_using_isbn, does_isbn_exist, match_books_by_string)
from models.users import (validate_and_get_details, User, create_new_user, 
                          is_full_name_invalid, is_username_invalid, 
                          username_already_exists, is_password_weak, get_full_name_from_id)
from models.user_books import insert_new_user_book, delete_user_book, total_fav_books, handle_pagination
from utils import generate_partial_uuid, generate_search_friendly_name
from werkzeug import secure_filename

app = Flask(__name__)
app.secret_key = '7834234dfasjfktsopbxdqmnsajfkss34343'
login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/', methods=['GET'])
def render_sign_in():
    if current_user.get_id():
        return redirect("/manage")
    else:
        return redirect("/sign_in")

@app.route('/motherlode/add', methods=['GET'])
def render_add_book_form():
    return render_template('add_books.html', title="Add Books")


@app.route('/motherlode/add', methods=['POST'])
def add_book():

    if 'book-title' not in request.form or is_book_invalid(request.form['book-title']):
        return "Book should have a name"

    if 'author' not in request.form or is_author_invalid(request.form['author']):
        return "Please specify the author's name"
    
    isbn = request.form['isbn']
    if 'isbn' not in request.form or is_isbn_invalid(isbn) or does_isbn_exist(isbn):
        return "Please mention the book's ISBN. No duplicates please."

    # Book cover
    if 'book-image' not in request.files or request.files['book-image'].filename == '':
        image_path_in_db = 'default-image.jpeg'

    elif is_cover_invalid(request.files['book-image'].filename):
        return "Improper image. Pleasefollow conventions"

    else:
        image_path_in_db = create_image_path_for_db(request.files['book-image'].filename)
        book_cover_file = request.files['book-image']
        # save file to FS
        book_cover_file.save(os.path.join('static', 'book_covers', image_path_in_db))
        
    book_to_save = Book(request.form['book-title'],
                        request.form['author'],
                        isbn.replace("-", ''),
                        image_path_in_db,
                        generate_search_friendly_name(request.form['book-title']))

    insert_new_book_to_motherlode(book_to_save)

    return redirect("/book/" + isbn)
    
class User_Auth(UserMixin):

    def __init__(self, id):
        self.id = id
        self.name = get_full_name_from_id(self.id)


    def __repr__(self):
        return "%d" % (self.id)

    def get_name(self):
        if self.get_id():
            return self.name
        else:
            return None


@login_manager.user_loader
def load_user(user_id):
    return User_Auth(user_id)


@app.route('/sign_in', methods=['GET'])
def render_sign_in_form():
    if current_user.get_id():
        return ('You are already logged in. Go <a href="/manage">manage</a> your books or <a href="/sign_out">logout</a>.')
    else:
        return render_template('sign_in.html', title="Sign In")

@app.route('/sign_in', methods=['POST'])
def sign_in(): 
    if 'username' in request.form and 'password' in request.form:
        # if validation fails return does not exist or something similar
        valid_sign_in, user_id, full_name = validate_and_get_details(request.form['username'], request.form['password'])

        if valid_sign_in:
            user = User_Auth(user_id)
            login_user(user)
            return redirect("/manage")
        else:
            return "The given user does not exist or you've entered an incorrect combination"
    else:
        return ("Please input an username and a password")


@app.route('/sign_out', methods=['GET'])
@login_required
def sign_out():
    full_name = current_user.get_name()
    logout_user()
    return (full_name + " has successfully logged out.")


@app.route('/sign_up', methods=['GET'])
def render_sign_up_form():
    return render_template('sign_up.html', title="Register")


@app.route('/sign_up', methods=['POST'])
def sign_up():

    if 'full-name' not in request.form or is_full_name_invalid(request.form['full-name']):
        return "Please enter full name"
    
    if 'username' not in request.form or is_username_invalid(request.form['username']) or username_already_exists(request.form['username']):
        return "Please enter your desired username"

    if 'password' not in request.form or is_password_weak(request.form['password']):
        return "Please enter a strong password"

    if 'repassword' not in request.form or request.form['password'] != request.form['repassword']:
        return "Please verify your password as well"

    user_to_create = User(request.form['full-name'],
                          request.form['username'],
                          request.form['password'])

    create_new_user(user_to_create)
    return ("user created")

@app.route('/book/<isbn>')
def book_details(isbn):
    isbn, name, author, image_path = get_details_using_isbn(isbn)
    return render_template("individual_book.html", title=name,
                            isbn=isbn, name=name, author=author,
                            image_path=image_path)

@app.route('/search/book/<name_string>')
def search_book_by_name(name_string):
    return jsonify(match_books_by_string(name_string))


@app.route('/manage', methods=['GET'])
def render_user_list():
    if current_user.get_id():
        return render_template("user_manage_books.html", title="Manage", full_name=current_user.get_name())
    else:
        return ("Please <a href='/sign_in'>login</a> if you want to continue.")


@app.route('/manage/add', methods=['POST'])
def add_favourite_book():
    id = current_user.get_id()
    if id:
        if is_isbn_invalid(request.form['isbn']):
            return ("Please enter a valid ISBN")
        if insert_new_user_book(id, request.form['isbn']):
            return ("Book successfully added")
        else:
            return ("Book could not be added due to various reasons")
    else:
        return ("Please <a href='/sign_in'>login</a> if you want to continue.")


# GET requests are cached by the browser. So choosing POST
@app.route('/manage/page/<int:page>', methods=['POST'])
def paginate_book_list(page):
    # have to rerender everytime as the items can change when
    # books are removed or inserted. It still does not take 
    # concurrency into account.

    # Take care of 0 and negative ints? Does Flask acknowledge negative ints?
    user_id = current_user.get_id()
    if user_id:
        total_books = total_fav_books(user_id)
        return jsonify(handle_pagination(user_id, page, total_books))
    else:
        return ("Please <a href='/sign_in'>login</a> if you want to continue.")

