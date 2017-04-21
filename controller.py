from flask import Flask


app = Flask(__name__)

@app.route('/', methods=['GET'])
def render_index():
    return("Hi", 200)