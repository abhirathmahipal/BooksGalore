# BooksGalore
Screening task for an internship at Metarvrse.  


## Good to Have
- Checks for extension and also verifies that it actually is a valid image file. Files renamed to jpeg to spoof an image file are rejected.
- Check via Ajax and get validations immediately. Probably try Flask flash
- Error messages instead of 'just' follow conventions.
- Image cropping and image size limit perhaps.
- Follow PEP8 and PEP20 standards everywhere (especially the import statements).
- React? I don't know if it will offer any advantage over Angular in *this* project but worth considering.
- Remove occurances of duplicate code if left accidentally.
- Try and catch statements.

## Reasoning Behind Decisions
- Chose Flask as Flask (with multithreads enabled) + gunicorn + nginx is decent for a sqlite databse. Also I'm more familiar with Flask than Django.
- I chose not to use an ORM and instead chose to write queries by hand as I felt it isn't that big a project.
- Why no proper commit messages? I forgot to commit in the start.
- Used a library called Flask-Login as manually setting and retrieving cookies would have been painful.

## References
Webpages that I found myself frequently going to.
- Python and Flask's documentations.
- http://getbootstrap.com/getting-started/#examples
- https://github.com/shekhargulati/flask-login-example/blob/master/flask-login-example.py
- Read about Angular and Flask interpolation since they use the same symbol
- GoodReads.com for image sizing help


## ```/motherlode/add```

### Name
- Server side and client side checks.  
### ISB
- Allows only numbers and hyphens. Strips away the hypens while saving it to the database. Checks for 13 digits.  
- Client side and server side.  
### Author
- Client side and server side.  
### Image 
- Client side and server side.  

## ```/sign_up```
- Password strength and username uniquess is verified before creating a new account.


## ```/manage```