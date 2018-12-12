import datetime
import pymysql

f1 = open('emergencyEnter.txt','w+')
f2 = open('emergencyExit.txt','w+')
conn = pymysql.connect(host='localhost',port=3306,user='root',password='2018',db = 'software7')
cursor = conn.cursor()

def emergency_enter_handler():
    while True:
        carNo = input('차량 번호 인식')
        if carNo == '복구':
            f1.seek(0)
            while True:
                RcarNo = f1.readline().strip('\n')
                if RcarNo == '':
                    print('복구 종료')
                    f1.close()
                    break
                else:
                    RTime = f1.readline().strip('\n')
                    RsectionNo = f1.readline().strip('\n')
                    sql = 'insert into parkinglot (carNo,sectionNo,parkingTime,currExist) values(%s,%s,%s,%s)'
                    cursor.execute(sql, (RcarNo, RsectionNo, RTime, 1))
                    sql2 = "UPDATE currParkinglot SET carNo = '%s', currExist = 1 WHERE sectionNo = '%s'" % (
                    RcarNo, RsectionNo)
                    cursor.execute(sql2)
                    conn.commit()
            break
        else:
            Time = datetime.datetime.now()
            sectionNo = input("(주차자리인식) ")
            f1.write(carNo)
            f1.write('\n')
            f1.write(str(Time))
            f1.write('\n')
            f1.write(sectionNo)
            f1.write('\n')

def emergency_exit_handler():
    while True:
        carNo = input('차량 번호 인식')
        Time =datetime.datetime.now()
        if carNo == '복구':
            f2.seek(0)
            while True:
                RcarNo = f2.readline().strip('\n')
                if RcarNo == '':
                    f2.close()
                    print('복구 종료')
                    break
                else:
                    RTime = f2.readline().strip('\n')
                    sql = 'update currparkinglot set carNo = %s , currExist = %s where carNo = %s'
                    cursor.execute(sql,(None,0,RcarNo))
                    sql2 = 'update parkinglot set exitTime = %s , currExist = %s where carNo = %s'
                    cursor.execute(sql2,(RTime,0,RcarNo))
                    conn.commit()
            break
        else:
            f2.write(carNo)
            f2.write('\n')
            f2.write(str(Time))
            f2.write('\n')

emergency_enter_handler()
#emergency_exit_handler()


