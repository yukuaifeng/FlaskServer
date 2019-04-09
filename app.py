from flask import Flask
from flask import render_template
from flask import Flask
from flask import jsonify
from flask_bootstrap import Bootstrap
import os


app = Flask(__name__)

basedir = os.path.dirname(__file__)

@app.route('/')
def hello_world():
    return render_template('Index.html')

@app.route('/query', methods=['GET', 'POST'])
def query():
    return render_template('display.html')

if __name__ == '__main__':
    app.run(debug=True)
