# BooksGalore
Screening task for an internship.

## Instructions
- You need to have Python2
- cd into the source directory
- Create a virtual environment named 'env' using  
```virtualenv -p "path/to/python2" env```  
- Install requirements ```pip install -r requirements.txt```
- If on Linux ```./start.sh```
- If on Windows open ```start.bat``` to start the server
- Extensively tested on Windows
- Inadequate testing on Linux
- This repository contains a sample database so that it's ready to use. If you don't want to use it delete ```booksgalore.db```
- Filler login credentials  
```abhirath``` - ```BJ123!```  
```rohan``` - ```BJ123!```
- ISBN's and usernames must be unique. Passwords should be atleast 6 characters long, must contain at least one numeric digis, one uppercase alphabet and one character from -> [!@#$^*.]


## Some Bugs and Smells
- User deleted from the DB for some reason but if the client still remembers the session associated with that user. The server isn't able to respond in this case.
- Should have taken out common functionality of preprocessing of input. chances of missing preprocessing somewhere due to this. For example ISBN when queried or inserted should always be stripped of all the hyphens. Bugs might arise as the stripping is done manually everywhere.
- Made a Book and User class. Didn't make proper use of it. Some queries use objects and other queries use strings or ints.
- Nasty frontend. Not organised at all. Eg: Angular directives and services could have been used for book cards instead of data binding.
- Routes (controller) isn't separated into different files.
- Concurrency issues (say the number of pages is 5. A little after that some new fav books are added. The client still think there are 5 pages till the next page is loaded). I haven't taken care of this issue.
- Frontend haven't accounted design for long book and author names.


## Good to Have
- Verify that it actually is a valid image file. Files renamed to jpeg to spoof an image file are rejected.
- Check via Ajax and get validations immediately. Probably try Flask flash
- Error messages instead of 'just' follow conventions.
- Image cropping and image size limit perhaps.
- Finish adding the votes section.
- Book comments in the individual books page.
- Follow PEP8 and PEP20 standards everywhere (especially the import statements).
- React? I don't know if it will offer any advantage over Angular in *this* project but worth considering.
- Remove occurances of duplicate code if left accidentally.
- **Code can be refactored in a lot of places.**
- Try and catch statements.
- The actual algorithms via which an ISBN can be checked (like how creditcard number are validated using certain rules).


## Reasoning Behind Decisions
- Chose Flask as Flask (with multithreads enabled) + gunicorn + nginx is decent for a sqlite databse. Also I'm more familiar with Flask than Django.
- I chose not to use an ORM and instead chose to write queries by hand as I felt it isn't that big a project.
- Why no proper commit messages? I forgot to commit in the start.
- Used a library called Flask-Login as manually setting and retrieving cookies would have been painful.
- Why an old version of Angular? I've used Angular 1.5 in the past and I felt it would save me some time.

## References
Webpages that I found myself frequently going to.
- Python and Flask's documentations
- http://getbootstrap.com/getting-started/#examples
- https://github.com/shekhargulati/flask-login-example/blob/master/flask-login-example.py
- Read about Angular and Flask interpolation since they use the same symbol
- GoodReads.com for book cover width to height ratio
- https://docs.python.org/2/library/sqlite3.html
- https://twitter.github.io/typeahead.js/examples/
- StackOverflow
- My old Angular project
- sqlite Python documentation and examples from tutorialspoint


## ```/motherlode/add```

### Name
- Server side and client side checks.  
### ISB
- Allows only numbers and hyphens. Strips away the hypens while saving it to the database. Checks for 13 digits.  
- Client side and server side.  
### Author
- Client side and server side.  
### Image 
- Client side and server side checks. Random strings are added at the end of an image file to avoid name collisions. Also a default image is used in case nothing is provided. 

## ```/sign_up```
- Password strength and username uniquess is verified before creating a new account.
- username can only contain alphanumeric characters. Max length of 15.
- Only hashed passwords are stored. The same hashing technique is used to compare passwords when a user tried to login.

## ```/manage```
- Users can see the list of his favourite books.
- When the user adds a favourite book, it checks the database if the book actually exists, if the user exists and doesn't insert if it's already in his fav list.
- Search for book via typeahead and add.
- User can delete a book from favourites.

## ```/book/<isbn>```
- Qucik stats about the book in question.
