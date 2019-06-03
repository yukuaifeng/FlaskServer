# -*- coding: utf-8 -*-
# author:yukuaifeng
# data:  2019/5/28 17:40

import pymysql
import pysnooper
from skfuzzy.cluster import cmeans
import numpy as np
import pandas as pd

db = pymysql.connect("localhost", "root", "950305", "evolution")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

#此函数已经不起作用，用于之前形成学校评分表，之后直接从评分表中获取数据，不再需要每次查询
# @pysnooper.snoop()
def produceSchoolRank():

    # sql = '''select school from grade_all where kind='理工类' and rank > 20000 group by school order by rank limit 50'''
    sql = '''select school from grade_all where kind='理工类' group by school '''

    cursor.execute(sql)

    schools = cursor.fetchall()

    schoolList = []
    schoolname = []
    for s in schools:
        schoolInfo = []
        # 首先拿到所有的学校的名字
        # 再根据学校名称找到它对应的地区，再根据地区得到对应的分数
        # 根据学校名称找到对应的综合实力排名
        # 根据学校名称找到对应的就业率排行名次
        # 根据学校名称找到科研经费的排名
        name = s[0]
        print(name)

        citySql = '''select city from school where name = '%s' ''' % name  # 这里注意要加入引号
        cursor.execute(citySql)
        city = cursor.fetchone()
        if city is None:
            nametmp = name.split("(")[0]
            citySql = '''select city from school where name = '%s' ''' % nametmp
            cursor.execute(citySql)
            city = cursor.fetchone()
            if city is None:
                nametmp = nametmp.replace("学院", "大学")
                citySql = '''select city from school where name = '%s' ''' % nametmp
                cursor.execute(citySql)
                city = cursor.fetchone()
        try:
            city = city[0]
        except TypeError:
            city = name[0:2]

        cityRankSql = '''select rank,grade from city_rank where city = '%s' ''' % city
        cursor.execute(cityRankSql)
        cityRank = cursor.fetchone()
        if cityRank is None:
            cityGrade = 0
            cityRank = 0
        else:
            cityGrade = cityRank[1]
            cityRank = cityRank[0]

        # 获取综合实力
        strengthSql = '''select grade from strength where school = '%s' ''' % name
        cursor.execute(strengthSql)
        strength = cursor.fetchone()
        if strength is None:
            strength = 60
        else:
            strength = strength[0]
        #strength = strength * 2

        # 获取就业率排名
        employmentSql = '''select grade from employment where school = '%s' ''' % name
        cursor.execute(employmentSql)
        employment = cursor.fetchone()
        if employment is None:
            employment = 25
        else:
            employment = employment[0]

        # 获取科研经费排名
        fundSql = '''select fund from funds where school = '%s' ''' % name
        cursor.execute(fundSql)
        fund = cursor.fetchone()
        if fund is None:
            fund = 1
        else:
            fund = fund[0]

        schoolInfo = [name, cityGrade, strength, employment, fund]
        schoolList.append(schoolInfo)
        schoolname.append(name)
    schooldf = pd.DataFrame(schoolList, columns=['school', 'cityGrade', 'strength', 'employment', 'fund'])
    schooldf.to_csv("schoolGrade.csv", encoding='utf_8_sig', index=False)

# schoolList, schoolname = getSchoolList(schools)

#@pysnooper.snoop()
def getSchoolList(schools, timelist):
    schoolList = []
    schoolName = []
    for school in schools:
        sql = '''select * from schoolgrade where school = '%s' ''' % school
        cursor.execute(sql)
        schoolgrade = cursor.fetchone()
        schoolgrade = list(schoolgrade)
        schoolName.append(schoolgrade[0])
        listtmp = schoolgrade[1:5]

        for i in range(0, len(timelist)):
            listtmp[i] = listtmp[i] * timelist[i]

        schoolList.append(listtmp)
    return schoolList, schoolName


def classify(schoolList, schoolname, num1, num2):
    schoolArray = np.array(schoolList)
    schoolArray.dtype = np.float64
    schoolArray = schoolArray.T

    center, u, u0, d, jm, p, fpc = cmeans(schoolArray, m=1.5, c=3, error=0.005, maxiter=1000)

    print(center)
    print(fpc)

    for i in u:
        label = np.argmax(u, axis=0)

    kind1 = []
    kind2 = []
    kind3 = []

    targetList1 = []
    targetList2 = []
    for row in center:
        targetList1.append(row[num1])
        targetList2.append(row[num2])

    kind_num1 = targetList1.index(max(targetList1))
    kind_num2 = targetList2.index(max(targetList2))

    for i in range(0, len(schoolList)):
        if label[i] == 0:
            kind1.append([schoolname[i], label[i]])
        elif label[i] == 1:
            kind2.append([schoolname[i], label[i]])
        else:
            kind3.append([schoolname[i], label[i]])

    return kind1, kind2, kind3, kind_num1, kind_num2

# kind1, kind2, kind3 = classify(schoolList, schoolname)
