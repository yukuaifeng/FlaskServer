# -*- coding: utf-8 -*-
# author:yukuaifeng
# data:  2019/6/26 9:29

import pandas as pd
from sqlalchemy import and_

from flaskserver.models import GradeLine

SCHOOL_NAME = []


def search_school(risk_result, sure_result, define_result):
    """
    提取出所有的学校的名称
    :param risk_result, sure_result, define_result:
    :return:SCHOOL_NAME
    """
    for dict_i in risk_result:
        SCHOOL_NAME.append(dict_i[0])

    for dict_i in sure_result:
        SCHOOL_NAME.append(dict_i[0])

    for dict_i in define_result:
        SCHOOL_NAME.append(dict_i[0])

    return SCHOOL_NAME


def output_school(school_name, grade, kind):
    """
    将筛选出来的学校的历史数据输出到excel中
    :param school_name:
    :param grade:
    :param kind:
    :return:
    """
    print(school_name)
    school_dataframe = pd.DataFrame(columns=['id', 'kind', 'number', 'school', 'year', 'figure',
                                             'grade', 'rank', 'chinese', 'math', 'english', 'clazz'])
    school_dataframe_2 = pd.DataFrame(columns=['school', '2018', '2017', '2016', '2015', '2014'])

    for name in school_name:
        ids = []
        kinds = []
        numbers = []
        schools = []
        years = []
        figures = []
        grades = []
        ranks = []
        chinese = []
        math = []
        english = []
        clazz = []
        school_info = GradeLine.query.filter(and_(GradeLine.school == name, GradeLine.year > 2013,
                                                  GradeLine.year <= 2018, GradeLine.kind == kind)).all()
        for info in school_info:
            ids.append(info.id)
            kinds.append(info.kind)
            numbers.append(info.number)
            schools.append(info.school)
            years.append(info.year)
            figures.append(info.figure)
            grades.append(info.grade)
            ranks.append(info.rank)
            chinese.append(info.chinese)
            math.append(info.math)
            english.append(info.english)
            clazz.append(info.clazz)

        new_rows = {'id': ids, 'kind': kinds, 'number': numbers, 'school': schools, 'year': years, 'figure': figures,
                    'grade': grades, 'rank': ranks, 'chinese': chinese, 'math': math, 'english': english,
                    'clazz': clazz}

        new_dataframe = pd.DataFrame(new_rows)

        if len(ranks) < 5:
            for i in range(0, 5-len(ranks)):
                ranks.append(0)

        print(ranks)
        new_rows_2 = {'school': schools[0], '2018': ranks[0], '2017': ranks[1], '2016': ranks[2], '2015': ranks[3],
                      '2014': ranks[4]}

        new_dataframe_2 = pd.DataFrame(new_rows_2, index=[0])

        school_dataframe = school_dataframe.append(new_dataframe, ignore_index=True)
        school_dataframe_2 = school_dataframe_2.append(new_dataframe_2, ignore_index=True)

    school_dataframe.columns = ['记录编号', '分科', '院校编号', '学校名称', '年份', '录取人数', '录取成绩',
                                '录取排名', '最低语文分数', '最低数学分数', '最低英语分数', '录取批次']
    out_path = "D:/Evaluation/output_results/湖南省%s%s分推荐学校.xls" % (kind, grade, )
    out_path_2 = "D:/Evaluation/output_results/湖南省%s%s分推荐学校(表2).xls" % (kind, grade, )

    school_dataframe.to_excel(out_path, index=False, encoding="utf_8_sig")
    school_dataframe_2.to_excel(out_path_2, index=False, encoding="utf_8_sig")


def output_school_info():
    schools = ['郑州工商学院', '大连交通大学', '辽宁对外经贸学院', '大连财经学院', '北京服装学院']
    school_dataframe = pd.DataFrame(columns=['school', '2018', '2017', '2016', '2015', '2014'])
    for name in schools:
        school_info = GradeLine.query.filter(and_(GradeLine.school == name, GradeLine.year > 2013,
                                                  GradeLine.year <= 2018, GradeLine.kind == '文史类')).all()
        ranks = []
        for info in school_info:
            ranks.append(info.rank)
        if len(ranks) < 5:
            for i in range(0, 5 - len(ranks)):
                ranks.append(0)

        print(ranks)
        new_rows_2 = {'school': name, '2018': ranks[0], '2017': ranks[1], '2016': ranks[2], '2015': ranks[3],
                      '2014': ranks[4]}

        new_dataframe_2 = pd.DataFrame(new_rows_2, index=[0])
        school_dataframe = school_dataframe.append(new_dataframe_2, ignore_index=True)
    out_path_2 = "D:/Evaluation/output_results/目标学校在湘招生（文科）排位情况表.xls"

    school_dataframe.to_excel(out_path_2, index=False, encoding="utf_8_sig")
