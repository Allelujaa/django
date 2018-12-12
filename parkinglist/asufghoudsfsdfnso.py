from django.db.models import Q
import datetime
import pymysql
from parkfunctions import admin
import random

def random_date(start, end):
        return start + datetime.timedelta(
                seconds=random.randint(0, int((end - start).total_seconds())),
        )

def random_select(a, b):
        if random.randint(0, 1) == 0:
                return a
        else:
                return b

conn = pymysql.connect(host='localhost', port=3306, user = 'root', password='2018', database = 'project7')
cursor = conn.cursor()

sql = """UPDATE currParkinglot SET carNo = %s, currExist = 1 WHERE sectionNo = %s"""

sqldelete = """DELETE FROM parkinglot"""

sqladd = """INSERT INTO parkinglot(carNo, sectionNo, parkingTime, exitTime, cost, currExist) VALUES(%s,%s,%s,%s,%s,%s)"""

sqlmember = """INSERT INTO client(carNo, clientNo, name) VALUES(%s, %s, %s)"""

for i in range(10):
        carNo = "carnumber" + str(i)
        clientNo = 1000 + i
        name = "KIM" + str(i)
        cursor.execute(sqlmember, (carNo, clientNo, name))
conn.commit()

# for idx in range(300):
#         carNo = "test" + str(idx)
#         if idx < 50:
#                 sectionNo = 'A' + str(idx + 10)
#         elif idx < 100:
#                 sectionNo = 'B' + str(idx - 50 + 10)
#         elif idx < 150:
#                 sectionNo = 'C' + str(idx - 100 + 10)
#         elif idx < 200:
#                 sectionNo = 'D' + str(idx - 150 + 10)
#         elif idx < 250:
#                 sectionNo = 'E' + str(idx - 200 + 10)
#         elif idx < 300:
#                 sectionNo = 'F' + str(idx - 250 + 10)
#         parkingTime = random_date(datetime.datetime(2017, 1, 1), datetime.datetime(2017, 12, 31))
#         exitTime = random_select(
#                 random_date(datetime.datetime(2018, 1, 1), datetime.datetime(2018, 12, 31)),
#                 None
#         )
#         cost = random.randint(0, 300000)
        
#         if exitTime == None:
#                 currExist = 1
#                 cursor.execute(sql, (carNo, sectionNo))

#         else:
#                 currExist = 0
        
#         cursor.execute(sqladd, (carNo, sectionNo, parkingTime, exitTime, cost, currExist))
        
# conn.commit()