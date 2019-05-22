from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint, abort, make_response
from flask_login import current_user

#from flaskserver.emails import send_new_comment_email, send_new_reply_email
from flaskserver.extensions import db
from flaskserver.forms import LoginForm, QueryForm
from flaskserver.models import User,Admission,GradeLine,ControlLine,StudentNumber
from flaskserver.utils import redirect_back
from sqlalchemy import text, and_
from . import choose
import pysnooper


server_bp = Blueprint('server', __name__)

@server_bp.route('/')
def index():
    form = QueryForm()
    return render_template('server/index.html', form=form)

@server_bp.route('/display')
def display(riskly_results):
    return render_template('server/display.html', riskly_results=riskly_results)

@server_bp.route('/query', methods=['GET','POST'])
#@pysnooper.snoop()
def query():
    queryform = QueryForm()
    if request.method == 'POST':

        kind = queryform.kind.data
        rank = queryform.rank.data
        grade = queryform.grade.data
        risk_num = queryform.risk_num.data
        sure_num = queryform.sure_num.data
        def_num = queryform.def_num.data

        # sql = "SELECT * FROM grade_line where rank > :rank group by school order by rank limit 100;"
        # testresults = db.session.execute(text(sql), {"rank": rank}).fetchall()
        # for result in testresults:
        #     print(result)

        kind_tmp = "理工类"
        if kind == '2':
            kind_tmp = "文史类"

        results = GradeLine.query.filter(GradeLine.kind == kind_tmp, GradeLine.rank > rank)\
            .group_by(GradeLine.school).order_by(GradeLine.rank).limit(50)

        riskly_results, surely_results, definite_results = choose.choose_school(results, rank, kind_tmp, risk_num, sure_num, def_num)
        #print(riskly_results, surely_results, definite_results)

        #return redirect(url_for(".display", riskly_results=riskly_results))
        return render_template('server/display.html', riskly_results=riskly_results, surely_results=surely_results, definite_results=definite_results)

    return render_template('server/index.html', form=queryform)





















