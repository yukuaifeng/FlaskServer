from flask import Flask
from flask import render_template

from flask import jsonify
import os


from flaskserver import create_app
app = create_app('production')
#app = Flask(__name__)

basedir = os.path.dirname(__file__)

# @app.route('/')
# def hello_world():
#     return render_template('server/index.html')
#
# @app.route('/query', methods=['GET', 'POST'])
# def query():
#     return render_template('server/display.html')

if __name__ == '__main__':
    app.run(debug=True)
