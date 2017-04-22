from controller import app
from config import path_to_db
import models.setup_db
import os


# If there's no DB, first make a DB
if not (os.path.isfile(path_to_db)):
    models.setup_db.setup()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)