# -*- coding: utf-8 -*-
# author:yukuaifeng
# data:  2019/5/21 15:35

import math
import numpy as np
from flaskserver.forms import LoginForm, QueryForm
from flaskserver.models import User,Admission,GradeLine,ControlLine,StudentNumber
from flaskserver.utils import redirect_back
from sqlalchemy import text, and_
import pysnooper

#@pysnooper.snoop()
def choose_school(results, rank, kind, risk_num, sure_num, def_num):
    #首先，循环得到的results，也就是里面的学校
    #循环体中，也就是每一个学校内，首先查询它的每一年的数据，存储在form中
    #然后进行四次运算：
    #首先是达到要求的年份占比计算
    #再就是计算五年内数据与目标rank的距离
    #然后就是五年内数据与高考人数、省控线距离的rank值
    schools = []
    rates = []
    clazzs = []
    riskly_results = []
    surely_results = []
    definite_results = []
    for result in results:
        schools.append(result.school)

    for school in schools:
        #首先通过学校的名称和满足rank的排名来获取学习的编号和批次
        #这里是因为有些学校的编号一致而批次不一样或者是学校名称一样但是录取的分数线同一年有多个
        schooltmp = GradeLine.query.filter(GradeLine.school == school, GradeLine.rank > rank).first()
        schoolnum = schooltmp.number
        schoolclazz = schooltmp.clazz
        #将所有的批次存入list中，之后存入字典里，方便查取
        clazzs.append(schoolclazz)

        #然后根据学校的编号和年份、分科和批次来查去相应地名次
        schoolForm = GradeLine.query.filter(and_(GradeLine.number == schoolnum, 2014 <= GradeLine.year,
                     GradeLine.year <= 2018, GradeLine.kind == kind, GradeLine.clazz == schoolclazz)).all()
        ranks = []
        years = []
        i = 0
        #存储该学校历年的录取排名，获得占比
        for s in schoolForm:
            ranks.append(s.rank)
            years.append(s.year)
            if s.rank > rank:
                i += 1

        #计算学校的历年排名与目标排名的距离
        distance = compute_distance(ranks, rank)
        number = i/len(schoolForm)

        stuNums = []
        ctrlRanks = []

        #通过年份来查询相应年份的对应的高考人数和省控线的排位
        #这里是因为不是每个学校的每一年数据都是完整的
        for year in years:
            Num = StudentNumber.query.filter(StudentNumber.year == year).first()
            stuNums.append(Num.stu_num)

            schoolrank = GradeLine.query.filter(and_(GradeLine.number == schoolnum, GradeLine.year == year,
                                                     GradeLine.kind == kind, GradeLine.clazz == schoolclazz)).first()
            schoolrank = schoolrank.rank
            ctrlrank = ControlLine.query.filter(and_(ControlLine.year == year, ControlLine.kind == kind,
                                                     ControlLine.ctrl_rank > schoolrank)).first()
            ctrlRanks.append(ctrlrank.ctrl_rank)

        #进行计算
        numVariance = compute_variance(ranks, stuNums)
        rankVariance = compute_variance(ranks, ctrlRanks)

        #如果学校的录取排名与目标排名差距过大，是因为目标名次数值太小，所以差距越小应该取值越小
        #但是要归一化到0-1的范围之中
        if distance > 1:
            distance = distance / (distance + 1)

        #这里是归一化均方差值
        #如果均方差过大，也是数值越小应该越好，归一化的值也应该越小
        if numVariance > 1:
            numVariance = numVariance / (numVariance + 1)

        if rankVariance > 1:
            rankVariance = rankVariance / (numVariance + 1)

        print(school)
        print(distance, number, numVariance, rankVariance)

        #然后将四个数据按照一定的比例将其计算出推荐的概率
        #因为占比肯定是最重要的，占比为78%
        #再就是与目标rank值之间的距离，占比为12%
        #其余的两项指标各占5%

        rate = (1-distance)*0.12 + number*0.78 + (1-numVariance)*0.05 + (1-rankVariance)*0.05

        rate = '%.2f%%' % (rate * 100)
        rates.append(rate)

    print(rates)
    clazzDict = dict(zip(schools, clazzs))
    schoolDict = dict(zip(schools, rates))


    #这里按照推荐概率对得到的结果进行分组
    riskly_dict = {k: v for k, v in schoolDict.items() if v < "80%"}
    surely_dict = {k: v for k, v in schoolDict.items() if "80%" < v < "90%"}
    definite_dict = {k: v for k, v in schoolDict.items() if v > "90%"}

    #然后对分组后的结果进行组内排序
    riskly_dict = sorted(riskly_dict.items(), key=lambda x: x[1], reverse=True)
    surely_dict = sorted(surely_dict.items(), key=lambda x: x[1], reverse=True)
    definite_dict = sorted(definite_dict.items(), key=lambda x: x[1], reverse=True)

    print(riskly_dict)

    #如果数目不够，就去找上面那个去借，再删除掉,避免重复
    #这里的情况是因为考虑到需要借的情况多是名次比较高的情况
    #所以将最接近目标的target的值借到上一个等级

    if len(riskly_dict) < risk_num:
        for i in range(0, risk_num-len(riskly_dict)):
            riskly_dict.append(surely_dict[-1-i])
            del surely_dict[i]

    if len(surely_dict) < sure_num:
        for i in range(0, sure_num-len(surely_dict)):
            surely_dict.append(definite_dict[-1-i])
            del definite_dict[i]

    # 加入录取批次，加入到相应地组内，与学校对应起来
    for i in range(0, len(riskly_dict)):
        riskly_dict[i] = riskly_dict[i] + (clazzDict[riskly_dict[i][0]],)

    for i in range(0, len(surely_dict)):
        surely_dict[i] = surely_dict[i] + (clazzDict[surely_dict[i][0]],)

    for i in range(0, len(definite_dict)):
        definite_dict[i] = definite_dict[i] + (clazzDict[definite_dict[i][0]],)

    #取出所需要的三项分类个数，这里的个数也是可以设置的
    for i in range(0, risk_num):
        riskly_results.append(riskly_dict[i])

    for i in range(0, sure_num):
        surely_results.append(surely_dict[i])

    for i in range(0, def_num):
        definite_results.append(definite_dict[i])

    # j = 0
    # for key in surely_dict:
    #     if j < 3:
    #         surely_results[key] = '%.2f%%' % (surely_dict[key] * 100)
    #         j += 1
    #     else:
    #         break
    #
    # n = 0
    # for key in definite_dict:
    #     if n < 4:
    #         definite_results[key] = '%.2f%%' % (definite_dict[key] * 100)
    #         n += 1
    #     else:
    #         break

    return riskly_results, surely_results, definite_results

#@pysnooper.snoop()
def compute_distance(ranks, rank):
    #把这个学校里的所有的录取名次和查询的名次进行求平方差再取均值
    #这里是采用范数，p=2
    tmp = 0.0
    for r in ranks:
        tmp += ((r-rank)/rank)**2
    distance = math.sqrt(tmp)/len(ranks)
    #distance = tmp/rank
    return distance

#@pysnooper.snoop()
def compute_variance(ranks, targets):
    #这里是要求所有的与高考的距离或者是与省控线的rank值的标准方差
    listtmp = [ranks[i] - targets[i] for i in range(len(ranks))]
    listtmp = [listtmp[i]/sum(listtmp) for i in range(len(listtmp))]
    if len(listtmp) == 1:
        variance = 1
    else:
        variance = np.std(listtmp, ddof=1)
#    print(variance)
    return variance