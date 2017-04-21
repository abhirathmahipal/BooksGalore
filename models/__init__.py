import os
from config import relative_path_to_db
import setup_db

# Check if DB exists. If not, create tables and a DB
if not (os.path.isfile(relative_path_to_db)):
    setup_db.setup()



