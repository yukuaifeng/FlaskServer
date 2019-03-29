from flask import Flask
from flask import render_template
from flask import Flask
from flask import jsonify
from flask_bootstrap import Bootstrap
import os


app = Flask(__name__)
bootstrap = Bootstrap(app)
basedir = os.path.dirname(__file__)

@app.route('/')
def hello_world():
    return render_template('test.html')


if __name__ == '__main__':
    app.run()