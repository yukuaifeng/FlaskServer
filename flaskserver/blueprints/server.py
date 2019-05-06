from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint, abort, make_response
from flask_login import current_user

#from flaskserver.emails import send_new_comment_email, send_new_reply_email
from flaskserver.extensions import db
from flaskserver.forms import LoginForm, QueryForm
from flaskserver.models import Admin,Admission
from flaskserver.utils import redirect_back

server_bp = Blueprint('flaskserver', __name__)

@server_bp.route('/')
def index():
    return render_template('server/index.html')

@server_bp.route('/query', methods=['GET','POST'])
def query():
    queryform = QueryForm()
    print(queryform.rank, queryform.grade.data)
    return render_template('server/display.html')