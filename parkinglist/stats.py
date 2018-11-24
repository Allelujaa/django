from django.db.models import Q
import datetime
import pymysql

conn = pymysql.connect(host='localhost', port=3306, user = 'root', password='2018', database = 'project7')
cursor = conn.cursor()

#매출: 총액, 평균 리턴
def sale_stats(datetime_start,datetime_end):  
    if datetime_start=='':
        if datetime_end=='':  #시작, 끝 모두 없음
            sql = "SELECT sum(cost), avg(cost) FROM parkinglot WHERE exitTime IS NOT NULL"
        else:    #끝 있음
            sql = "SELECT sum(cost), avg(cost) FROM parkinglot WHERE exitTime<='%s'"%datetime_end
    else: #시작 있음
        if datetime_end=='':
            sql = "SELECT sum(cost), avg(cost) FROM parkinglot WHERE exitTime>='%s'"%datetime_start
        else:    #시작, 끝 둘다 있음
            sql = "SELECT sum(cost), avg(cost) FROM parkinglot WHERE (exitTime BETWEEN '%s' AND '%s')"%(datetime_start, datetime_end)
    cursor.execute(sql)
    data = cursor.fetchall()
    return data

#차량 통계: 차량별 주차장 이용횟수, 총금액, 평균 금액
def car_stats(datetime_start,datetime_end):
    if datetime_start=='':
        if datetime_end=='':  #시작, 끝 모두 없음
            sql = "SELECT carNo,count(*),sum(cost),avg(cost) FROM parkinglot WHERE exitTime IS NOT NULL GROUP BY carNo"
        else:    #끝 있음
            sql = "SELECT carNo,count(*),sum(cost),avg(cost) FROM parkinglot WHERE exitTime<='%s' GROUP BY carNo"%datetime_end
    else:   #시작 있음
        if datetime_end=='':
            sql = "SELECT carNo,count(*),sum(cost),avg(cost) FROM parkinglot WHERE exitTime>='%s' GROUP BY carNo"%datetime_start
        else:    #시작, 끝 둘다 있음
            sql = "SELECT carNo,count(*),sum(cost),avg(cost) FROM parkinglot WHERE (exitTime BETWEEN '%s' AND '%s') GROUP BY carNo"%(datetime_start, datetime_end)
    cursor.execute(sql)
    data = cursor.fetchall()
    return data

#구역 통계: 구역별 총 차량 수, 총 금액 리턴
def section_stats(datetime_start,datetime_end):  
    section_list = ['A%','B%','C%','D%','E%','F%']
    data_list = []  #A,B,C,D,E,F 각 구역별 주차했던 총 차량 수, 총 금액 저장 Ex.[23,450000,42,430000,...] 2개씩 해당 구역의 총차량수와 총금액
    if datetime_start=='':
        if datetime_end=='':  #시작, 끝 모두 없음
            for section in section_list:
                sql = "SELECT count(*),sum(cost) FROM parkinglot WHERE exitTime IS NOT NULL and sectionNo LIKE '%s'"%section
                cursor.execute(sql)
                for row in cursor:
                    data_list.append(row[0]), data_list.append(row[1])
        else:    #끝 있음
            for section in section_list:
                sql = "SELECT count(*),sum(cost) FROM parkinglot WHERE exitTime<='%s' and sectionNo LIKE '%s'"%(datetime_end,section)
                cursor.execute(sql)
                for row in cursor:
                    data_list.append(row[0]), data_list.append(row[1])  
    else:
        if datetime_end=='':  #시작 있음
            for section in section_list:
                sql = "SELECT count(*),sum(cost) FROM parkinglot WHERE exitTime>='%s' and sectionNo LIKE '%s'"%(datetime_start,section)
                cursor.execute(sql)
                for row in cursor:
                    data_list.append(row[0]), data_list.append(row[1])
        else:    #시작, 끝 둘다 있음
            for section in section_list:
                sql = "SELECT count(*),sum(cost) FROM parkinglot WHERE (exitTime BETWEEN '%s' AND '%s') and sectionNo LIKE '%s'"%(datetime_start, datetime_end, section)
                cursor.execute(sql)
                for row in cursor:
                    data_list.append(row[0]), data_list.append(row[1])
    return data_list

    
#사용자 통계: 총 고객수, 총 금액, 총 일반 고객수, 일반 고객수의 총 금액, 총 회원 고객수, 총 회원 고객수의 총 금액 리턴   
def user_stats(datetime_start,datetime_end):     
    if datetime_start=='':
        if datetime_end=='':  #시작, 끝 모두 없음
            sql =  """SELECT count(*), sum(cost) FROM parkinglot WHERE exitTime IS NOT NULL
            union all
            SELECT count(*), sum(cost) FROM parkinglot WHERE carNo not in (SELECT distinct carNo FROM client) and exitTime IS NOT NULL
            union all
            SELECT count(*), sum(cost) FROM parkinglot p, client c WHERE p.carNo = c.carNo and exitTime IS NOT NULL"""
        else:  # 끝 있음
            sql = """SELECT count(*), sum(cost) FROM parkinglot WHERE exitTime<='%s'
            union all
            SELECT count(*), sum(cost) FROM parkinglot WHERE carNo not in (SELECT distinct carNo FROM client) and exitTime<='%s'
            union all
            SELECT count(*), sum(cost) FROM parkinglot p, client c WHERE p.carNo = c.carNo and exitTime<='%s'"""%(datetime_end, datetime_end, datetime_end)
    else:  # 시작 있음
        if datetime_end=='':
            sql =  """SELECT count(*), sum(cost) FROM parkinglot WHERE exitTime>='%s'
            union all
            SELECT count(*), sum(cost) FROM parkinglot WHERE carNo not in (SELECT distinct carNo FROM client) and exitTime>='%s'
            union all
            SELECT count(*), sum(cost) FROM parkinglot p, client c WHERE p.carNo = c.carNo and exitTime>='%s'"""%(datetime_start, datetime_start, datetime_start)
        else:  # 시작, 끝 둘다 있음
            sql = """SELECT count(*), sum(cost) FROM parkinglot WHERE (exitTime BETWEEN '%s' AND '%s')
            union all
            SELECT count(*), sum(cost) FROM parkinglot WHERE carNo not in (SELECT distinct carNo FROM client) and (exitTime BETWEEN '%s' AND '%s')
            union all
            SELECT count(*), sum(cost) FROM parkinglot p, client c WHERE p.carNo = c.carNo and (exitTime BETWEEN '%s' AND '%s')"""%(datetime_start, datetime_end, datetime_start, datetime_end, datetime_start, datetime_end)
    cursor.execute(sql)
    data = cursor.fetchall()
    return data

