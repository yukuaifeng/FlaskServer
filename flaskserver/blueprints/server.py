from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint, abort, make_response
from flask_login import current_user

#from flaskserver.emails import send_new_comment_email, send_new_reply_email
from flaskserver.extensions import db
from flaskserver.forms import LoginForm, QueryForm
from flaskserver.models import Admin,Admission
from flaskserver.utils import redirect_back
from sqlalchemy import text
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

        # sql = "SELECT * FROM grade_line where rank > :rank group by school order by rank limit 100;"
        # testresults = db.session.execute(text(sql), {"rank": rank}).fetchall()
        # for result in testresults:
        #     print(result)

        results = Admission.query.filter(Admission.kind == '理科', Admission.rank > rank)\
            .group_by(Admission.school).order_by(Admission.rank).limit(50)

        riskly_results, surely_results, definite_results = choose_school(results, rank)
        print(riskly_results, surely_results, definite_results)

        #return redirect(url_for(".display", riskly_results=riskly_results))
        return render_template('server/display.html', riskly_results=riskly_results, surely_results=surely_results, definite_results=definite_results)

    return render_template('server/index.html', form=queryform)

#@pysnooper.snoop()
def compute(ranks, rank, variance):
    tmp = 0.0
    for r in ranks:
        for i in r:
            tmp += (i-rank)**2
        tmp = tmp/5
        variance.append(tmp)
    return variance



#@pysnooper.snoop()
def choose_school(results, rank):
    #先把找出来的所有学校拿出来放在一起
    #再新建五个数组，按年份个数，放置录取名次大于输入名次的学校
    #循环查询每个学校，按学校查询出所有的录取名次，找出大于目标名次的个数
    #将对应的学校的所有录取名次也要放在一个list里面，二维list
    #再新建五个list，将对应分组里的学校里的录取名次与目标名次的标准差求方差和
    #按照方差和从小到大进行排序，拿出相应的学校
    all_school = []
    count_1, count_2, count_3, count_4, count_5 = ([] for i in range(5))
    ranks_1, ranks_2, ranks_3, ranks_4, ranks_5 = ([] for i in range(5))
    variance_1, variance_2, variance_3, variance_4, variance_5 = ([] for i in range(5))
    riskly_results, surely_results, definite_results = ([] for i in range(3))
    for result in results:
        all_school.append(result.school)
        single_school = Admission.query.filter(Admission.school == result.school, Admission.kind == '理科').all()
        i = 0
        ranks_tmp = []
        for s in single_school:
            ranks_tmp.append(s.rank)
            if s.rank > rank:
                i += 1

        if i == 1:
            count_1.append(result.school)
            ranks_1.append(ranks_tmp)
        elif i == 2:
            count_2.append(result.school)
            ranks_2.append(ranks_tmp)
        elif i == 3:
            count_3.append(result.school)
            ranks_3.append(ranks_tmp)
        elif i == 4:
            count_4.append(result.school)
            ranks_4.append(ranks_tmp)
        elif i == 5:
            count_5.append(result.school)
            ranks_5.append(ranks_tmp)

    #计算不同分组内的每一个学校历年的录取名次和目标名次的差距的均方差
    variance_1 = compute(ranks_1, rank, variance_1)
    variance_2 = compute(ranks_2, rank, variance_2)
    variance_3 = compute(ranks_3, rank, variance_3)
    variance_4 = compute(ranks_4, rank, variance_4)
    variance_5 = compute(ranks_5, rank, variance_5)


    #将学校名称和学校的均方差联系起来，组成字典
    dict_1 = dict(zip(count_1, variance_1))
    dict_2 = dict(zip(count_2, variance_2))
    dict_3 = dict(zip(count_3, variance_3))
    dict_4 = dict(zip(count_4, variance_4))
    dict_5 = dict(zip(count_5, variance_5))

    #将只有1,2两个组合在一起，用来筛选冲的这些选项，只有3,4两个组合在一起，用来筛选稳的这些选项
    dict_risk = dict(dict_1, **dict_2)
    dict_sure = dict(dict_3, **dict_4)

    #将三个字典按照value，也就是均方差的值进行排序
    sorted(dict_risk.items(), key=lambda item: item[1])
    sorted(dict_sure.items(), key=lambda item: item[1])
    sorted(dict_5.items(), key=lambda item: item[1])

    #下面就是选出需要的个数
    i = 0
    j = 0
    k = 0
    for key in dict_risk:
        if i > 2:
            break
        riskly_results.append(key)
        i += 1

    for key in dict_sure:
        if j > 2:
            break
        surely_results.append(key)
        j += 1

    for key in dict_5:
        if k > 3:
            break
        definite_results.append(key)
        k += 1

    return riskly_results, surely_results, definite_results








