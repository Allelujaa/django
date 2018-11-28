import pymysql
import datetime
from dateutil.relativedelta import *
from django.db.models import Q
import os
from . import connector

conn = connector.con()
cursor = conn.cursor()

# visualize()는 현재 주차장을 표시한 2d 배열을 반환합니다.
# 배열은 3(구역)x10(행)x10(열) 이고, 데이터는 'num', 'exist'으로 구성된 dictionary입니다.
def visualize():
    sql = 'SELECT sectionNo, carNo, currExist FROM currParkinglot'
    cursor.execute(sql)
    currentlot = cursor.fetchall()
    # for spot in currentlot
    # spot[0] --> sectionNo
    # spot[1] --> carNo
    # spot[2] --> currExist
    
    # car2darray[3][10][10]
    car2darray = [[[{'num': '', 'exist': ''} for i in range(10)] for j in range(10)] for k in range(3)]

    for spot in currentlot:
        # sectionNos that start with A, C, E take the first half of the area
        # sectionNos that start with B, D, F take the other half
        if spot[0][0] in 'ACE':
            x = int(spot[0][2])
            y = int(spot[0][1]) - 1
        elif spot[0][0] in 'BDF':
            x = int(spot[0][2])
            y = int(spot[0][1]) + 4
            
        # sectionNos that start with A, B --> car2darray[0]
        # sectionNos that start with C, D --> car2darray[1]
        # sectionNos that start with E, F --> car2darray[2]
        if spot[0][0] in 'AB':
            car2darray[0][x][y] = {'num': spot[0], 'exist': spot[2]}
        elif spot[0][0] in 'CD':
            car2darray[1][x][y] = {'num': spot[0], 'exist': spot[2]}
        elif spot[0][0] in 'EF':
            car2darray[2][x][y] = {'num': spot[0], 'exist': spot[2]}
    
    
    return car2darray

# carcount(area)는 현재 주차장 area에 있는 차량의 개수를 반환합니다.
# area1 -> A, B
# area2 -> C, D
# area3 -> E, F
def carcount(area):
    if area == 1:
        val = ['A%%', 'B%%']
    elif area == 2:
        val = ['C%%', 'D%%']
    elif area == 3:
        val = ['E%%', 'F%%']
    sql = 'SELECT * FROM currParkinglot WHERE currExist = ''1'' AND sectionNo LIKE %s'
    
    count = cursor.execute(sql, val[0])
    count += cursor.execute(sql, val[1])
    
    return count

# show_records(start, until)는 parkinglot에서 start번부터 until번 row를 tuple 형태로 반환합니다.
def show_records(start, until):
    sql = "SELECT * from parkinglot limit %s, %s"
    cursor.execute(sql, (start, until))
    
    return cursor.fetchall()

# count_records()는 parkinglot의 row 개수를 반환합니다.
def count_records():
    sql = 'SELECT * FROM parkinglot'
    count = cursor.execute(sql)
    
    return count

# check_overTime()은 주차한지 1년이상 됐으며 퇴장하지 않은 차의 정보를 tuple 형태로 반환합니다.
def check_overTime():
    year_before = datetime.datetime.now() - relativedelta(years=1)
    sql = "SELECT carNo from parkinglot where currExist = 1 and parkingTime<=%s"
    cursor.execute(sql, year_before)
    
    return cursor.fetchall()

# delete_overTime()은 check_overTime()에서 확인된 차량들을 
#   1. currParkinglot에서 제거하고,
#   2. parkinglot에서 currExist를 0으로 바꿉니다.
#   3. 퇴장시간은 기록하지 않습니다.
def delete_overTime():
    for idx in check_overTime():
        sql = "UPDATE currParkinglot set currExist = %s, carNo = %s where carNo = %s"
        sql2 = "UPDATE parkinglot set currExist = %s where carNo = %s"
        cursor.execute(sql, (0, None, idx[0]))
        cursor.execute(sql2, (0, idx[0]))
    conn.commit()
    

# advanced_search()는 특수검색을 위한 q object를 반환합니다.
def advanced_search():
    q = Q()
    if cardata != '': #차량번호 조건 있을 때
        q &= Q(carno=cardata)

    if in_datetime_start != None:
        if in_datetime_end != None:  #시작과 끝 범위 모두 있음
            q &= Q(parkingtime__range=(in_datetime_start, in_datetime_end))
        else: q &= Q(parkingtime__gte=in_datetime_start) #시작만 있음
    elif in_datetime_end != None: q &= Q(parkingtime__lte=in_datetime_end) #끝만 있음

    if out_datetime_start != None:
        if out_datetime_end != None: #시작과 끝 범위 모두 있음
            q &= Q(exittime__range=(out_datetime_start, out_datetime_end))
        else: q &= Q(exittime__gte=out_datetime_start)#시작만 있음
    elif out_datetime_end != None: q &= Q(exittime__lte=out_datetime_end)#끝만 있음

    if cost_min != None:
        if cost_max != None:
            q &= Q(cost__range=(cost_min, cost_max))  #cost_min과 cost_max 모두 있음
        else: q &= Q(cost__gte=min_cost) #cost_min있음
    elif cost_max != None:  q &= Q(cost__lte=max_cost) #cost_max 있음

    if sectionno != '':  #주차 구역 조건 있을 때
        q &= Q(sectionno=sectionno)

    if exists != '':   #현재 유무 조건 있을 때
        q &= Q(currexist=int(exists))
    
    return q