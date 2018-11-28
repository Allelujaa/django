import datetime
from dateutil.relativedelta import *
import pymysql
import os
from . import connector

conn = connector.con()
cursor = conn.cursor()

def check_overTime():
    year_before = datetime.datetime.now() - relativedelta(years=1)
    sql = "SELECT carNo from parkinglot where currExist = 1 and parkingTime<=%s"
    cursor.execute(sql, year_before)
    data = cursor.fetchall()
    
    return data

def delete_overTime():
    for idx in check_overTime():
        sql = "UPDATE currParkinglot set currExist = %s, carNo = %s where carNo = %s"
        sql2 = "UPDATE parkinglot set currExist = %s where carNo = %s"
        cursor.execute(sql, (0, None, idx[0]))
        cursor.execute(sql2, (0, idx[0]))
    conn.commit()
    